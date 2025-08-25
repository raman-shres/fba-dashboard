# app/services/bsr_model.py

from __future__ import annotations

def est_monthly_sales(bsr: int | None, category: str | None = None) -> int:
    """
    Very simple placeholder mapping from BSR (Best Sellers Rank) to
    estimated monthly sales. Replace with category-specific curves later.

    Args:
        bsr: Current sales rank (lower is better). None or <= 0 returns 0.
        category: Optional Amazon category (unused for now).

    Returns:
        Estimated units sold per month (integer).
    """
    if bsr is None or bsr <= 0:
        return 0

    # crude, order-of-magnitude tiers
    if bsr <= 1_000:
        return 1_200
    if bsr <= 5_000:
        return 600
    if bsr <= 20_000:
        return 200
    if bsr <= 100_000:
        return 50
    return 10
