from __future__ import annotations


def discounted_total(prices: list[float], discount_pct: float) -> float:
    """Return the discounted total for a list of prices."""
    if discount_pct < 0 or discount_pct > 100:
        raise ValueError("discount_pct must be between 0 and 100")
    total = sum(prices)
    return total * (1.0 - discount_pct / 100.0)
