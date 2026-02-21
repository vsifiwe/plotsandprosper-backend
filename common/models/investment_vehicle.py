"""
Investment vehicle model — tracks where pooled group funds are invested.
"""

from django.db import models


class InvestmentVehicleType(models.TextChoices):
    """
    Investment vehicle type choices.
    """

    SAVINGS_ACCOUNT = "SAVINGS_ACCOUNT", "Savings Account"
    LAND = "LAND", "Land"
    SHARES = "SHARES", "Shares"
    GOVERNMENT_BOND = "GOVERNMENT_BOND", "Government Bond"
    OTHER = "OTHER", "Other"


class InvestmentVehicle(models.Model):
    """
    Represents an investment channel used by the group.
    """

    name = models.CharField(max_length=128)
    vehicle_type = models.CharField(
        max_length=32,
        choices=InvestmentVehicleType.choices,
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """
        Meta class for InvestmentVehicle.
        """

        ordering = ["-created_at"]
        verbose_name = "Investment vehicle"
        verbose_name_plural = "Investment vehicles"

    def __str__(self):
        """
        String representation of the investment vehicle.
        """
        return f"{self.name} ({self.get_vehicle_type_display()})"
