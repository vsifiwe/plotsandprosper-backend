"""
MemberShareAllocation model — immutable record of per-member share ownership in a vehicle.
"""

from django.db import models


class MemberShareAllocation(models.Model):
    """
    Immutable record of a member's share allocation in a share-based vehicle.
    Positive shares = buy, negative shares = sell/redeem.
    No update/delete allowed — corrections via new entries only.
    """

    member = models.ForeignKey(
        "common.Member",
        on_delete=models.PROTECT,
        related_name="share_allocations",
    )
    investment_vehicle = models.ForeignKey(
        "common.InvestmentVehicle",
        on_delete=models.PROTECT,
        related_name="member_allocations",
    )
    shares = models.DecimalField(max_digits=20, decimal_places=4)
    share_price = models.DecimalField(max_digits=20, decimal_places=4)
    amount = models.DecimalField(max_digits=20, decimal_places=4)
    investment_event = models.ForeignKey(
        "common.InvestmentEvent",
        on_delete=models.PROTECT,
        related_name="member_allocations",
        null=True,
        blank=True,
    )
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]
        verbose_name = "Member share allocation"
        verbose_name_plural = "Member share allocations"

    def __str__(self):
        return (
            f"{self.shares} shares of {self.investment_vehicle.name} "
            f"for {self.member.firstName} {self.member.lastName}"
        )
