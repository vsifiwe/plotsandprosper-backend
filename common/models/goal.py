"""
Goal model for member financial targets.
"""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class GoalTimeline(models.TextChoices):
    """
    Supported goal timeline choices.
    """

    SIX_MONTHS = "6_MONTHS", "6 months"
    ONE_YEAR = "1_YEAR", "1 year"
    TWO_YEARS = "2_YEARS", "2 years"
    FIVE_YEARS = "5_YEARS", "5 years"
    TEN_YEARS = "10_YEARS", "10 years"


class Goal(models.Model):
    """
    One active financial goal per member.
    """

    member = models.OneToOneField(
        "common.Member",
        on_delete=models.CASCADE,
        related_name="goal",
    )
    timeline = models.CharField(max_length=16, choices=GoalTimeline.choices)
    target_amount = models.DecimalField(
        max_digits=20,
        decimal_places=4,
        validators=[MinValueValidator(Decimal("0.0001"))],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        verbose_name = "Goal"
        verbose_name_plural = "Goals"

    def __str__(self):
        return (
            f"{self.member.firstName} {self.member.lastName} - "
            f"{self.target_amount} in {self.get_timeline_display()}"
        )
