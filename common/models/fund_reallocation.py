"""
FundReallocation model — immutable record of moving funds between investment vehicles.
"""

from django.db import models


class FundReallocationStatus(models.TextChoices):
    """
    Fund reallocation status choices.
    """

    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    COMPLETED = "COMPLETED", "Completed"


class FundReallocation(models.Model):
    """
    Immutable record of a fund transfer from one investment vehicle to another.
    No update/delete allowed — corrections via new entries only.
    """

    source_vehicle = models.ForeignKey(
        "common.InvestmentVehicle",
        on_delete=models.PROTECT,
        related_name="reallocations_out",
    )
    destination_vehicle = models.ForeignKey(
        "common.InvestmentVehicle",
        on_delete=models.PROTECT,
        related_name="reallocations_in",
    )
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    status = models.CharField(
        max_length=16,
        choices=FundReallocationStatus.choices,
        default=FundReallocationStatus.PENDING,
    )
    requested_by = models.ForeignKey(
        "common.Member",
        on_delete=models.PROTECT,
        related_name="fund_reallocations",
    )
    reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """
        Meta class for FundReallocation
        """

        ordering = ["-created_at"]
        verbose_name = "Fund reallocation"
        verbose_name_plural = "Fund reallocations"

    def __str__(self):
        """
        String representation of the fund reallocation
        """

        return (
            f"Reallocation of {self.amount} "
            f"from {self.source_vehicle.name} to {self.destination_vehicle.name}"
        )
