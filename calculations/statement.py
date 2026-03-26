"""
calculations/statement.py

Pure financial functions for member investment statements — no DB access.
"""

from decimal import Decimal, ROUND_HALF_UP


def compute_portfolio_summary(lifetime_contributions, current_portfolio_value):
    """
    Compute portfolio-level summary metrics for a member.

    Args:
        lifetime_contributions: Total contributions made by the member (Decimal, must be >= 0).
        current_portfolio_value: Current total value of all positions (Decimal, must be >= 0).

    Returns:
        Dict with lifetime_contributions, current_portfolio_value, total_gain_loss,
        and return_percentage (quantized to 2 decimal places).

    Raises:
        ValueError: If either input is negative.
    """
    if lifetime_contributions < Decimal("0"):
        raise ValueError("Lifetime contributions cannot be negative.")

    if current_portfolio_value < Decimal("0"):
        raise ValueError("Current portfolio value cannot be negative.")

    total_gain_loss = current_portfolio_value - lifetime_contributions

    if lifetime_contributions > Decimal("0"):
        return_percentage = (
            (total_gain_loss / lifetime_contributions) * Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        return_percentage = Decimal("0.00")

    return {
        "lifetime_contributions": lifetime_contributions,
        "current_portfolio_value": current_portfolio_value,
        "total_gain_loss": total_gain_loss,
        "return_percentage": return_percentage,
    }


def compute_share_position(total_shares, book_value, current_nav):
    """
    Compute position metrics for a member's holdings in a share-based vehicle.

    Args:
        total_shares: Total shares owned by the member (Decimal, must be > 0).
        book_value: Total cost basis / book value of shares (Decimal, must be >= 0).
        current_nav: Current NAV per share (Decimal, must be > 0).

    Returns:
        Dict with shares_owned, book_value, average_entry_nav, current_nav,
        current_value, unrealized_gain_loss, and return_percentage.

    Raises:
        ValueError: If validation fails.
    """
    if total_shares <= Decimal("0"):
        raise ValueError("Total shares must be greater than zero.")

    if book_value < Decimal("0"):
        raise ValueError("Book value cannot be negative.")

    if current_nav <= Decimal("0"):
        raise ValueError("Current NAV must be greater than zero.")

    average_entry_nav = (book_value / total_shares).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    current_value = (total_shares * current_nav).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )
    unrealized_gain_loss = current_value - book_value

    if book_value > Decimal("0"):
        return_percentage = (
            (unrealized_gain_loss / book_value) * Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        return_percentage = Decimal("0.00")

    return {
        "shares_owned": total_shares,
        "book_value": book_value,
        "average_entry_nav": average_entry_nav,
        "current_nav": current_nav,
        "current_value": current_value,
        "unrealized_gain_loss": unrealized_gain_loss,
        "return_percentage": return_percentage,
    }


def compute_asset_position(
    ownership_percentage, equity_value, cash_distributed, cash_pending, total_cost_basis
):
    """
    Compute position metrics for a member's stake in a non-share vehicle (land, etc.).

    Args:
        ownership_percentage: Member's ownership percentage (Decimal).
        equity_value: Current equity value of the member's stake (Decimal, must be >= 0).
        cash_distributed: Cash already distributed to the member (Decimal, must be >= 0).
        cash_pending: Cash pending distribution (Decimal, must be >= 0).
        total_cost_basis: Original amount the member invested (Decimal, must be >= 0).

    Returns:
        Dict with ownership_percentage, current_equity, unrealized_value,
        cash_distributed, cash_pending, realized_gain, total_position_value,
        and total_return_percentage.

    Raises:
        ValueError: If validation fails.
    """
    if equity_value < Decimal("0"):
        raise ValueError("Equity value cannot be negative.")

    if cash_distributed < Decimal("0"):
        raise ValueError("Cash distributed cannot be negative.")

    if cash_pending < Decimal("0"):
        raise ValueError("Cash pending cannot be negative.")

    if total_cost_basis < Decimal("0"):
        raise ValueError("Total cost basis cannot be negative.")

    total_position_value = equity_value + cash_distributed + cash_pending
    realized_gain = cash_distributed

    if total_cost_basis > Decimal("0"):
        total_return_percentage = (
            ((total_position_value - total_cost_basis) / total_cost_basis)
            * Decimal("100")
        ).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    else:
        total_return_percentage = Decimal("0.00")

    return {
        "ownership_percentage": ownership_percentage,
        "current_equity": equity_value,
        "unrealized_value": equity_value,
        "cash_distributed": cash_distributed,
        "cash_pending": cash_pending,
        "realized_gain": realized_gain,
        "total_position_value": total_position_value,
        "total_return_percentage": total_return_percentage,
    }
