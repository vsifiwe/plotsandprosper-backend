"""
AssetOwnershipRecord model — immutable record of per-member equity stake in a non-share vehicle.
"""

from decimal import Decimal

from django.db import models


class AssetOwnershipRecord(models.Model):
    """
    Immutable record of a member's equity stake in a non-share vehicle (land, etc.).
    New records are appended when ownership changes.
    No update/delete allowed.
    """

    member = models.ForeignKey(
        "common.Member",
        on_delete=models.PROTECT,
        related_name="asset_ownership_records",
    )
    investment_vehicle = models.ForeignKey(
        "common.InvestmentVehicle",
        on_delete=models.PROTECT,
        related_name="ownership_records",
    )
    ownership_percentage = models.DecimalField(max_digits=10, decimal_places=4)
    equity_value = models.DecimalField(max_digits=20, decimal_places=4)
    cash_distributed = models.DecimalField(
        max_digits=20, decimal_places=4, default=Decimal("0.0000")
    )
    cash_pending = models.DecimalField(
        max_digits=20, decimal_places=4, default=Decimal("0.0000")
    )
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]
        verbose_name = "Asset ownership record"
        verbose_name_plural = "Asset ownership records"

    def __str__(self):
        return (
            f"{self.ownership_percentage}% of {self.investment_vehicle.name} "
            f"for {self.member.firstName} {self.member.lastName}"
        )
