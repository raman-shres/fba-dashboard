# app/services/keepa.py

from __future__ import annotations
from typing import Any, Dict, List

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.config import settings

BASE = "https://api.keepa.com"


class KeepaConfigError(RuntimeError):
    pass


def _require_api_key() -> str:
    key = settings.keepa_api_key
    if not key:
        raise KeepaConfigError(
            "KEEPA_API_KEY is missing. Add it to backend/.env as KEEPA_API_KEY=YOUR_KEY and restart."
        )
    return key


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=8),
    retry=retry_if_exception_type((httpx.TransportError, httpx.ReadTimeout)),
)
async def _fetch_products_chunk(client: httpx.AsyncClient, asins_chunk: List[str]) -> Dict[str, Any]:
    params = {
        "key": _require_api_key(),
        "domain": "1",           # 1 = US marketplace
        "asin": ",".join(asins_chunk),
        "history": "0",          # set to "1" later if you need historical data
    }
    resp = await client.get(f"{BASE}/product", params=params)
    resp.raise_for_status()
    return resp.json()


async def fetch_keepa_by_asins(asins: List[str]) -> Dict[str, Any]:
    """
    Fetch product data for a list of ASINs from Keepa.
    Returns a dict with at least a 'products' list.
    """
    if not asins:
        return {"products": []}

    # Be conservative about request size; chunk large lists.
    CHUNK = 50
    products: List[Dict[str, Any]] = []

    async with httpx.AsyncClient(timeout=30) as client:
        for i in range(0, len(asins), CHUNK):
            chunk = asins[i : i + CHUNK]
            data = await _fetch_products_chunk(client, chunk)
            products.extend(data.get("products", []))

    return {"products": products}
