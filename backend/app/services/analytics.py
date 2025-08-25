# app/services/analytics.py

from __future__ import annotations

from math import isfinite


def estimate_referral_fee_pct(category: str | None) -> float:
    """
    Placeholder: Amazon referral fees vary by category (~8–15%+).
    For now, return a flat 15%. Replace with category-specific logic later.
    """
    return 0.15


def estimate_fba_fees(
    weight_lb: float | None = None,
    dims_in: tuple[float, float, float] | None = None,
) -> float:
    """
    Placeholder: flat FBA fulfillment fee until a real calculator is wired in.
    """
    return 4.00


def compute_profit(
    price: float,
    cost: float,
    referral_fee_pct: float,
    fba_fees: float,
) -> float:
    """
    Profit per unit after Amazon referral + FBA fees.
    """
    fees = price * referral_fee_pct + fba_fees
    return round(price - cost - fees, 2)


def compute_roi(
    price: float,
    cost: float,
    referral_fee_pct: float,
    fba_fees: float,
) -> float:
    """
    ROI = profit / cost. Returns 0.0 if cost is 0 to avoid division by zero.
    """
    profit = compute_profit(price, cost, referral_fee_pct, fba_fees)
    return round((profit / cost) if cost else 0.0, 4)


def risk_band_from_roi(roi: float) -> str:
    """
    Buckets ROI into LOW/MEDIUM/HIGH risk bands (simple heuristic).
    """
    if not isfinite(roi):
        return "unknown"
    if roi >= 0.5:
        return "LOW"
    if roi >= 0.2:
        return "MEDIUM"
    return "HIGH"
