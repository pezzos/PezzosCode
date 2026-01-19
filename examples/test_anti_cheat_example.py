import random

import pytest

from examples.anti_cheat_example import discounted_total


def test_discounted_total_with_fixtures():
    fixtures = [
        ([10.0, 5.0], 0.0, 15.0),
        ([10.0, 5.0], 50.0, 7.5),
        ([2.5, 7.5, 10.0], 20.0, 16.0),
    ]

    for prices, discount_pct, expected in fixtures:
        assert discounted_total(prices, discount_pct) == pytest.approx(expected)


def test_discounted_total_invariants_seeded():
    rng = random.Random(1337)
    for _ in range(50):
        prices = [rng.uniform(0.01, 100.0) for _ in range(rng.randint(1, 10))]
        discount_pct = rng.uniform(0.0, 100.0)
        total = discounted_total(prices, discount_pct)
        raw_total = sum(prices)

        assert 0.0 <= total <= raw_total + 1e-9
        assert total == pytest.approx(raw_total * (1.0 - discount_pct / 100.0))


def test_discounted_total_rejects_invalid_discount():
    with pytest.raises(ValueError):
        discounted_total([1.0], -1.0)
    with pytest.raises(ValueError):
        discounted_total([1.0], 101.0)
