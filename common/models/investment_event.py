"""
InvestmentEvent model — immutable record of investing funds into a vehicle.
"""

from django.db import models


class InvestmentEvent(models.Model):
    """
    Immutable record of investing funds from the unallocated pool into a vehicle.
    No update/delete allowed — corrections via new entries only.
    """

    investment_vehicle = models.ForeignKey(
        "common.InvestmentVehicle",
        on_delete=models.PROTECT,
        related_name="investment_events",
    )
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    shares = models.DecimalField(max_digits=20, decimal_places=4)
    share_price = models.DecimalField(max_digits=20, decimal_places=4)
    recorded_by = models.ForeignKey(
        "common.Member",
        on_delete=models.PROTECT,
        related_name="recorded_investments",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class for InvestmentEvent.
        """

        ordering = ["-created_at"]
        verbose_name = "Investment event"
        verbose_name_plural = "Investment events"

    def __str__(self):
        """
        String representation of the investment event.
        """
        return f"Investment of {self.amount} into {self.investment_vehicle.name}"
