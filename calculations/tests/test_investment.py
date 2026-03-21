"""
Tests for calculations.investment — pure financial logic, no DB.
"""

import pytest
from decimal import Decimal

from calculations.investment import (
    compute_contribution_allocation,
    compute_investment_balances,
)


class TestComputeContributionAllocation:
    def test_basic_allocation(self):
        result = compute_contribution_allocation(
            Decimal("5000.0000"), Decimal("1000.0000")
        )
        assert result == Decimal("6000.0000")

    def test_allocation_from_zero(self):
        result = compute_contribution_allocation(
            Decimal("0.0000"), Decimal("2500.0000")
        )
        assert result == Decimal("2500.0000")

    def test_fractional_amount(self):
        result = compute_contribution_allocation(
            Decimal("1000.5050"), Decimal("250.2525")
        )
        assert result == Decimal("1250.7575")

    def test_zero_amount_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            compute_contribution_allocation(Decimal("5000.0000"), Decimal("0"))

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            compute_contribution_allocation(Decimal("5000.0000"), Decimal("-100.0000"))


class TestComputeInvestmentBalances:
    def test_basic_investment(self):
        new_unalloc, new_vehicle = compute_investment_balances(
            Decimal("10000.0000"),
            Decimal("5000.0000"),
            Decimal("3000.0000"),
            Decimal("30.0000"),
            Decimal("100.0000"),
        )
        assert new_unalloc == Decimal("7000.0000")
        assert new_vehicle == Decimal("8000.0000")

    def test_full_balance_investment(self):
        new_unalloc, new_vehicle = compute_investment_balances(
            Decimal("5000.0000"),
            Decimal("0.0000"),
            Decimal("5000.0000"),
            Decimal("500.0000"),
            Decimal("10.0000"),
        )
        assert new_unalloc == Decimal("0.0000")
        assert new_vehicle == Decimal("5000.0000")

    def test_fractional_shares(self):
        new_unalloc, new_vehicle = compute_investment_balances(
            Decimal("10000.0000"),
            Decimal("2000.0000"),
            Decimal("1500.0000"),
            Decimal("7.5000"),
            Decimal("200.0000"),
        )
        assert new_unalloc == Decimal("8500.0000")
        assert new_vehicle == Decimal("3500.0000")

    def test_insufficient_funds_raises(self):
        with pytest.raises(ValueError, match="Insufficient unallocated funds"):
            compute_investment_balances(
                Decimal("1000.0000"),
                Decimal("5000.0000"),
                Decimal("2000.0000"),
                Decimal("20.0000"),
                Decimal("100.0000"),
            )

    def test_zero_amount_raises(self):
        with pytest.raises(ValueError, match="Investment amount must be greater than zero"):
            compute_investment_balances(
                Decimal("10000.0000"),
                Decimal("5000.0000"),
                Decimal("0"),
                Decimal("10.0000"),
                Decimal("100.0000"),
            )

    def test_negative_amount_raises(self):
        with pytest.raises(ValueError, match="Investment amount must be greater than zero"):
            compute_investment_balances(
                Decimal("10000.0000"),
                Decimal("5000.0000"),
                Decimal("-500.0000"),
                Decimal("5.0000"),
                Decimal("100.0000"),
            )

    def test_zero_shares_raises(self):
        with pytest.raises(ValueError, match="Shares must be greater than zero"):
            compute_investment_balances(
                Decimal("10000.0000"),
                Decimal("5000.0000"),
                Decimal("1000.0000"),
                Decimal("0"),
                Decimal("100.0000"),
            )

    def test_negative_shares_raises(self):
        with pytest.raises(ValueError, match="Shares must be greater than zero"):
            compute_investment_balances(
                Decimal("10000.0000"),
                Decimal("5000.0000"),
                Decimal("1000.0000"),
                Decimal("-10.0000"),
                Decimal("100.0000"),
            )

    def test_zero_share_price_raises(self):
        with pytest.raises(ValueError, match="Share price must be greater than zero"):
            compute_investment_balances(
                Decimal("10000.0000"),
                Decimal("5000.0000"),
                Decimal("1000.0000"),
                Decimal("10.0000"),
                Decimal("0"),
            )

    def test_negative_share_price_raises(self):
        with pytest.raises(ValueError, match="Share price must be greater than zero"):
            compute_investment_balances(
                Decimal("10000.0000"),
                Decimal("5000.0000"),
                Decimal("1000.0000"),
                Decimal("10.0000"),
                Decimal("-100.0000"),
            )

    def test_amount_mismatch_raises(self):
        with pytest.raises(ValueError, match="Amount mismatch"):
            compute_investment_balances(
                Decimal("10000.0000"),
                Decimal("5000.0000"),
                Decimal("999.0000"),
                Decimal("10.0000"),
                Decimal("100.0000"),
            )
