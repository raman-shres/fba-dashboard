# app/api/routes.py

from __future__ import annotations

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services import cache as c
from app.services.analytics import (
    estimate_referral_fee_pct,
    estimate_fba_fees,
    compute_roi,
    compute_profit,
    risk_band_from_roi,
)
from app.services.bsr_model import est_monthly_sales
from app.services.monte_carlo import run_profit_sim
from app.services.keepa import fetch_keepa_by_asins, KeepaConfigError

import csv
import io
from typing import List, Dict, Any


router = APIRouter()


# ---------- Pydantic models ----------

class AnalyzeItem(BaseModel):
    asin: str
    cost: float
    price_override: float | None = None
    category: str | None = None
    bsr: int | None = None


class AnalyzeRequest(BaseModel):
    items: List[AnalyzeItem]


# ---------- Health check ----------

@router.get("/health")
async def health():
    return {"ok": True}


# ---------- Analyze ASINs ----------

@router.post("/asins/analyze")
async def analyze_asins(
    payload: AnalyzeRequest,
    db: AsyncSession = Depends(get_db),  # kept for future DB usage
):
    # Build a cache key that changes when inputs change
    key = "analyze:" + ";".join(
        [f"{i.asin}:{i.cost}:{i.price_override}" for i in payload.items]
    )

    # --- Try cache (fail-open if Redis not available) ---
    cached = None
    try:
        cached = c.cache_get(key)
    except Exception as e:
        print(f"[WARN] cache_get failed: {e}")
    if cached:
        return {"cached": True, "data": cached}

    # --- Fetch Keepa (fail-open if no key or network error) ---
    asins = [i.asin for i in payload.items]
    keepa: Dict[str, Any] = {"products": []}
    try:
        keepa = await fetch_keepa_by_asins(asins)
    except KeepaConfigError as e:
        print(f"[WARN] Keepa key missing: {e} — continuing without Keepa data")
    except Exception as e:
        print(f"[WARN] Keepa fetch failed: {e} — continuing without Keepa data")

    # Map Keepa response → dict by ASIN
    keepa_by_asin: Dict[str, Dict[str, Any]] = {}
    for p in keepa.get("products", []):
        keepa_by_asin[p.get("asin")] = {
            "title": p.get("title"),
            "category": str(p.get("productType", "")),
            "bsr": p.get("stats", {}).get("currentSalesRank"),
            "buybox": (p.get("buyBoxSellerId") is not None),
            "price": (p.get("stats", {}).get("buyBoxPrice") or 0) / 100.0,
        }

    # Compute analytics per item
    out: List[Dict[str, Any]] = []
    for item in payload.items:
        kp = keepa_by_asin.get(item.asin, {})
        category = item.category or kp.get("category")
        price = item.price_override or kp.get("price") or 0.0
        bsr = item.bsr or kp.get("bsr")

        referral_pct = estimate_referral_fee_pct(category)
        fba_fee = estimate_fba_fees()
        roi = compute_roi(price, item.cost, referral_pct, fba_fee)
        profit_unit = compute_profit(price, item.cost, referral_pct, fba_fees=fba_fee)
        sales_m = est_monthly_sales(bsr, category)

        sim = run_profit_sim(
            price_mean=price,
            price_std=max(price * 0.05, 0.1),
            monthly_sales_mean=sales_m,
            monthly_sales_std=max(sales_m * 0.2, 1.0),
            cost=item.cost,
            referral_fee_pct=referral_pct,
            fba_fees=fba_fee,
            runs=10_000,
        )

        out.append(
            {
                "asin": item.asin,
                "title": kp.get("title"),
                "category": category,
                "price": round(price, 2),
                "cost": item.cost,
                "roi": roi,
                "profit_per_unit": profit_unit,
                "risk_band": risk_band_from_roi(roi),
                "bsr": bsr,
                "est_monthly_sales": sales_m,
                "sim": sim,
            }
        )

    # Try to cache (fail-open)
    try:
        c.cache_set(key, out, ttl_seconds=300)
    except Exception as e:
        print(f"[WARN] cache_set failed: {e}")

    return {"cached": False, "data": out}


# ---------- CSV upload (batch preview) ----------

@router.post("/batches/upload")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file")

    content = await file.read()
    text = content.decode("utf-8", errors="ignore")
    reader = csv.DictReader(io.StringIO(text))

    items: List[Dict[str, Any]] = []
    for row in reader:
        # Expect headers: asin,cost,price_override (price_override optional)
        items.append(
            {
                "asin": (row.get("asin") or "").strip(),
                "cost": float(row.get("cost") or 0),
                "price_override": (float(row.get("price_override") or 0) or None),
            }
        )

    return {"ok": True, "count": len(items), "preview": items[:10]}
