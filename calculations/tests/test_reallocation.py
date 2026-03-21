"""
Tests for calculations.reallocation — pure financial logic, no DB.
"""

import pytest
from decimal import Decimal

from calculations.reallocation import compute_reallocation_balances


class TestComputeReallocationBalances:
    def test_basic_reallocation(self):
        new_src, new_dst = compute_reallocation_balances(
            Decimal("10000.0000"), Decimal("5000.0000"), Decimal("3000.0000")
        )
        assert new_src == Decimal("7000.0000")
        assert new_dst == Decimal("8000.0000")

    def test_full_balance_reallocation(self):
        new_src, new_dst = compute_reallocation_balances(
            Decimal("5000.0000"), Decimal("2000.0000"), Decimal("5000.0000")
        )
        assert new_src == Decimal("0.0000")
        assert new_dst == Decimal("7000.0000")

    def test_destination_starts_at_zero(self):
        new_src, new_dst = compute_reallocation_balances(
            Decimal("8000.0000"), Decimal("0.0000"), Decimal("3000.0000")
        )
        assert new_src == Decimal("5000.0000")
        assert new_dst == Decimal("3000.0000")

    def test_fractional_amount(self):
        new_src, new_dst = compute_reallocation_balances(
            Decimal("1000.5050"), Decimal("200.2500"), Decimal("500.2525")
        )
        assert new_src == Decimal("500.2525")
        assert new_dst == Decimal("700.5025")

    def test_insufficient_funds_raises(self):
        with pytest.raises(ValueError, match="Insufficient funds"):
            compute_reallocation_balances(
                Decimal("1000.0000"), Decimal("5000.0000"), Decimal("1500.0000")
            )

    def test_zero_amount_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            compute_reallocation_balances(
                Decimal("1000.0000"), Decimal("5000.0000"), Decimal("0")
            )

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            compute_reallocation_balances(
                Decimal("1000.0000"), Decimal("5000.0000"), Decimal("-100.0000")
            )
