"""
common/views/analytics.py
"""

from datetime import timedelta
from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Sum
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Contribution, InvestmentVehicle, Member


class GroupAnalyticsView(APIView):
    """
    Return high-level group analytics statistics.
    """

    CONTRIBUTION_GROWTH_WINDOW_DAYS = 30

    def get(self, request):
        """
        Get key analytics metrics for the group.
        """
        now = timezone.now()
        current_window_start = now - timedelta(days=self.CONTRIBUTION_GROWTH_WINDOW_DAYS)
        previous_window_start = current_window_start - timedelta(
            days=self.CONTRIBUTION_GROWTH_WINDOW_DAYS
        )

        total_contributions = (
            Contribution.objects.aggregate(total=Sum("amount"))["total"] or Decimal("0")
        )
        current_window_total = (
            Contribution.objects.filter(
                recorded_at__gte=current_window_start,
                recorded_at__lt=now,
            ).aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
        )
        previous_window_total = (
            Contribution.objects.filter(
                recorded_at__gte=previous_window_start,
                recorded_at__lt=current_window_start,
            ).aggregate(total=Sum("amount"))["total"]
            or Decimal("0")
        )

        growth_rate = self._calculate_growth_rate(
            previous_total=previous_window_total,
            current_total=current_window_total,
        )

        return Response(
            {
                "memberCount": Member.objects.count(),
                "totalContributions": str(total_contributions),
                "totalInvestments": InvestmentVehicle.objects.count(),
                "growthRate": float(growth_rate),
            }
        )

    def _calculate_growth_rate(self, previous_total, current_total):
        """
        Calculate percentage growth between two periods.
        """
        if previous_total == 0:
            if current_total == 0:
                return Decimal("0.00")
            return Decimal("100.00")

        growth = ((current_total - previous_total) / previous_total) * Decimal("100")
        return growth.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
