"""
NAVRecord model — immutable point-in-time NAV snapshot for share-based vehicles.
"""

from django.db import models


class NAVRecord(models.Model):
    """
    Immutable point-in-time NAV (Net Asset Value) per share for a vehicle.
    Used to compute current market value of member holdings.
    No update/delete allowed.
    """

    investment_vehicle = models.ForeignKey(
        "common.InvestmentVehicle",
        on_delete=models.PROTECT,
        related_name="nav_records",
    )
    nav_per_share = models.DecimalField(max_digits=20, decimal_places=4)
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]
        verbose_name = "NAV record"
        verbose_name_plural = "NAV records"

    def __str__(self):
        return f"NAV {self.nav_per_share} for {self.investment_vehicle.name} at {self.recorded_at}"
