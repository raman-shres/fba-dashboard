# app/services/monte_carlo.py

from __future__ import annotations
from typing import Any, Optional, Dict

import numpy as np


def run_profit_sim(
    *,
    price_mean: float,
    price_std: float,
    monthly_sales_mean: float,
    monthly_sales_std: float,
    cost: float,
    referral_fee_pct: float,
    fba_fees: float,
    runs: int = 10_000,
    seed: Optional[int] = None,
    hist_bins: int = 40,
) -> Dict[str, Any]:
    """
    Monte Carlo simulation of monthly profit.

    We draw `runs` samples for price and monthly sales from (truncated) normal
    distributions, compute unit profit and multiply by sampled sales to get a
    monthly profit distribution. Returns P5/P50/P95 and a histogram useful for
    Plotly/Chart.js.

    Notes:
      • Uses vectorized math (fast) instead of per-sample Python loops.
      • Clamps to avoid negative prices/sales.
      • `seed` makes runs reproducible for testing.
    """
    rng = np.random.default_rng(seed)

    # Draw samples (avoid zero std which can cause warnings)
    price_std = max(price_std, 1e-9)
    sales_std = max(monthly_sales_std, 1e-9)

    prices = rng.normal(price_mean, price_std, runs)
    sales = rng.normal(monthly_sales_mean, sales_std, runs)

    # Truncate to valid domain
    prices = np.clip(prices, 0.01, None)  # no free items
    sales = np.clip(sales, 0.0, None)     # can't sell negative units

    # Vectorized unit profit (same formula as compute_profit, without rounding)
    fees = prices * referral_fee_pct + fba_fees
    unit_profit = prices - cost - fees

    monthly_profit = unit_profit * sales

    # Percentiles
    p5 = float(np.percentile(monthly_profit, 5))
    p50 = float(np.percentile(monthly_profit, 50))
    p95 = float(np.percentile(monthly_profit, 95))

    # Histogram for charting
    counts, edges = np.histogram(monthly_profit, bins=hist_bins)
    hist = {"counts": counts.tolist(), "edges": edges.tolist()}

    return {
        "p5": round(p5, 2),
        "p50": round(p50, 2),
        "p95": round(p95, 2),
        "hist": hist,
    }
