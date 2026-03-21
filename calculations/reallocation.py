"""
calculations/reallocation.py

Pure financial functions for fund reallocation — no DB access.
"""

from decimal import Decimal


def compute_reallocation_balances(source_value, destination_value, amount):
    """
    Compute new balances after reallocating *amount* from source to destination.

    Args:
        source_value: Current value of the source vehicle (Decimal).
        destination_value: Current value of the destination vehicle (Decimal).
        amount: Amount to transfer (Decimal, must be > 0).

    Returns:
        Tuple of (new_source_value, new_destination_value).

    Raises:
        ValueError: If amount is negative/zero or exceeds source balance.
    """
    if amount <= Decimal("0"):
        raise ValueError("Reallocation amount must be greater than zero.")

    if amount > source_value:
        raise ValueError(
            f"Insufficient funds in source vehicle. "
            f"Available: {source_value}, requested: {amount}."
        )

    new_source_value = source_value - amount
    new_destination_value = destination_value + amount
    return new_source_value, new_destination_value
