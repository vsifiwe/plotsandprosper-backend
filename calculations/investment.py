"""
calculations/investment.py

Pure financial functions for contribution allocation and investment events — no DB access.
"""

from decimal import Decimal


def compute_contribution_allocation(unallocated_value, contribution_amount):
    """
    Compute new unallocated balance after receiving a contribution.

    Args:
        unallocated_value: Current unallocated pool balance (Decimal).
        contribution_amount: Amount of the new contribution (Decimal, must be > 0).

    Returns:
        New unallocated balance (Decimal).

    Raises:
        ValueError: If contribution_amount is zero or negative.
    """
    if contribution_amount <= Decimal("0"):
        raise ValueError("Contribution amount must be greater than zero.")

    return unallocated_value + contribution_amount


def compute_investment_balances(unallocated_value, vehicle_value, shares, share_price):
    """
    Compute new balances after investing from the unallocated pool into a vehicle.
    Amount is derived from shares * share_price.

    Args:
        unallocated_value: Current unallocated pool balance (Decimal).
        vehicle_value: Current value of the target vehicle (Decimal).
        shares: Number of shares purchased (Decimal, must be > 0).
        share_price: Price per share (Decimal, must be > 0).

    Returns:
        Tuple of (amount, new_unallocated_value, new_vehicle_value).

    Raises:
        ValueError: If any validation fails.
    """
    if shares <= Decimal("0"):
        raise ValueError("Shares must be greater than zero.")

    if share_price <= Decimal("0"):
        raise ValueError("Share price must be greater than zero.")

    amount = shares * share_price

    if amount > unallocated_value:
        raise ValueError(
            f"Insufficient unallocated funds. "
            f"Available: {unallocated_value}, requested: {amount}."
        )

    new_unallocated = unallocated_value - amount
    new_vehicle = vehicle_value + amount
    return amount, new_unallocated, new_vehicle
