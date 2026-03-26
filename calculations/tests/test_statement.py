"""
Tests for calculations.statement — pure financial logic, no DB.
"""

import pytest
from decimal import Decimal

from calculations.statement import (
    compute_portfolio_summary,
    compute_share_position,
    compute_asset_position,
)


class TestComputePortfolioSummary:
    def test_basic_gain(self):
        result = compute_portfolio_summary(
            Decimal("1950000.0000"), Decimal("2049508.0000")
        )
        assert result["lifetime_contributions"] == Decimal("1950000.0000")
        assert result["current_portfolio_value"] == Decimal("2049508.0000")
        assert result["total_gain_loss"] == Decimal("99508.0000")
        assert result["return_percentage"] == Decimal("5.10")

    def test_basic_loss(self):
        result = compute_portfolio_summary(
            Decimal("1000000.0000"), Decimal("900000.0000")
        )
        assert result["total_gain_loss"] == Decimal("-100000.0000")
        assert result["return_percentage"] == Decimal("-10.00")

    def test_zero_contributions(self):
        result = compute_portfolio_summary(
            Decimal("0.0000"), Decimal("0.0000")
        )
        assert result["total_gain_loss"] == Decimal("0.0000")
        assert result["return_percentage"] == Decimal("0.00")

    def test_zero_portfolio_value(self):
        result = compute_portfolio_summary(
            Decimal("500000.0000"), Decimal("0.0000")
        )
        assert result["total_gain_loss"] == Decimal("-500000.0000")
        assert result["return_percentage"] == Decimal("-100.00")

    def test_negative_contributions_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            compute_portfolio_summary(Decimal("-100.0000"), Decimal("0.0000"))

    def test_negative_portfolio_value_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            compute_portfolio_summary(Decimal("100.0000"), Decimal("-50.0000"))

    def test_breakeven(self):
        result = compute_portfolio_summary(
            Decimal("1000000.0000"), Decimal("1000000.0000")
        )
        assert result["total_gain_loss"] == Decimal("0.0000")
        assert result["return_percentage"] == Decimal("0.00")


class TestComputeSharePosition:
    def test_basic_position_with_gain(self):
        result = compute_share_position(
            total_shares=Decimal("3176.8000"),
            book_value=Decimal("750000.0000"),
            current_nav=Decimal("267.4100"),
        )
        assert result["shares_owned"] == Decimal("3176.8000")
        assert result["book_value"] == Decimal("750000.0000")
        assert result["average_entry_nav"] == Decimal("236.09")
        assert result["current_nav"] == Decimal("267.4100")
        assert result["current_value"] == Decimal("849508.09")
        assert result["unrealized_gain_loss"] == Decimal("99508.09")
        assert result["return_percentage"] == Decimal("13.27")

    def test_position_with_loss(self):
        result = compute_share_position(
            total_shares=Decimal("100.0000"),
            book_value=Decimal("50000.0000"),
            current_nav=Decimal("400.0000"),
        )
        assert result["current_value"] == Decimal("40000.00")
        assert result["unrealized_gain_loss"] == Decimal("-10000.00")
        assert result["return_percentage"] == Decimal("-20.00")

    def test_fractional_shares(self):
        result = compute_share_position(
            total_shares=Decimal("0.5000"),
            book_value=Decimal("100.0000"),
            current_nav=Decimal("250.0000"),
        )
        assert result["average_entry_nav"] == Decimal("200.00")
        assert result["current_value"] == Decimal("125.00")

    def test_zero_shares_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            compute_share_position(
                Decimal("0.0000"), Decimal("1000.0000"), Decimal("100.0000")
            )

    def test_negative_shares_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            compute_share_position(
                Decimal("-10.0000"), Decimal("1000.0000"), Decimal("100.0000")
            )

    def test_negative_book_value_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            compute_share_position(
                Decimal("10.0000"), Decimal("-1000.0000"), Decimal("100.0000")
            )

    def test_zero_nav_raises(self):
        with pytest.raises(ValueError, match="greater than zero"):
            compute_share_position(
                Decimal("10.0000"), Decimal("1000.0000"), Decimal("0.0000")
            )

    def test_zero_book_value(self):
        result = compute_share_position(
            total_shares=Decimal("10.0000"),
            book_value=Decimal("0.0000"),
            current_nav=Decimal("100.0000"),
        )
        assert result["average_entry_nav"] == Decimal("0.00")
        assert result["return_percentage"] == Decimal("0.00")


class TestComputeAssetPosition:
    def test_basic_land_position_no_return(self):
        """Matches the PDF example: Bugesera land at 6% ownership, no gains yet."""
        result = compute_asset_position(
            ownership_percentage=Decimal("6.0000"),
            equity_value=Decimal("1200000.0000"),
            cash_distributed=Decimal("0.0000"),
            cash_pending=Decimal("0.0000"),
            total_cost_basis=Decimal("1200000.0000"),
        )
        assert result["ownership_percentage"] == Decimal("6.0000")
        assert result["current_equity"] == Decimal("1200000.0000")
        assert result["unrealized_value"] == Decimal("1200000.0000")
        assert result["cash_distributed"] == Decimal("0.0000")
        assert result["cash_pending"] == Decimal("0.0000")
        assert result["realized_gain"] == Decimal("0.0000")
        assert result["total_position_value"] == Decimal("1200000.0000")
        assert result["total_return_percentage"] == Decimal("0.00")

    def test_position_with_distributed_cash(self):
        result = compute_asset_position(
            ownership_percentage=Decimal("10.0000"),
            equity_value=Decimal("500000.0000"),
            cash_distributed=Decimal("50000.0000"),
            cash_pending=Decimal("0.0000"),
            total_cost_basis=Decimal("400000.0000"),
        )
        assert result["total_position_value"] == Decimal("550000.0000")
        assert result["realized_gain"] == Decimal("50000.0000")
        assert result["total_return_percentage"] == Decimal("37.50")

    def test_position_with_pending_cash(self):
        result = compute_asset_position(
            ownership_percentage=Decimal("5.0000"),
            equity_value=Decimal("300000.0000"),
            cash_distributed=Decimal("0.0000"),
            cash_pending=Decimal("25000.0000"),
            total_cost_basis=Decimal("300000.0000"),
        )
        assert result["total_position_value"] == Decimal("325000.0000")
        assert result["total_return_percentage"] == Decimal("8.33")

    def test_zero_cost_basis(self):
        result = compute_asset_position(
            ownership_percentage=Decimal("5.0000"),
            equity_value=Decimal("100000.0000"),
            cash_distributed=Decimal("0.0000"),
            cash_pending=Decimal("0.0000"),
            total_cost_basis=Decimal("0.0000"),
        )
        assert result["total_return_percentage"] == Decimal("0.00")

    def test_negative_equity_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            compute_asset_position(
                Decimal("5.0000"), Decimal("-100.0000"),
                Decimal("0.0000"), Decimal("0.0000"), Decimal("0.0000"),
            )

    def test_negative_cash_distributed_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            compute_asset_position(
                Decimal("5.0000"), Decimal("100000.0000"),
                Decimal("-100.0000"), Decimal("0.0000"), Decimal("100000.0000"),
            )

    def test_negative_cash_pending_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            compute_asset_position(
                Decimal("5.0000"), Decimal("100000.0000"),
                Decimal("0.0000"), Decimal("-100.0000"), Decimal("100000.0000"),
            )

    def test_negative_cost_basis_raises(self):
        with pytest.raises(ValueError, match="cannot be negative"):
            compute_asset_position(
                Decimal("5.0000"), Decimal("100000.0000"),
                Decimal("0.0000"), Decimal("0.0000"), Decimal("-100.0000"),
            )
