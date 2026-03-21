"""
common/views/contribution.py
"""

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from calculations.investment import compute_contribution_allocation
from common.models import Contribution, InvestmentVehicle, InvestmentVehicleType
from common.serializers import ContributionSerializer
from common.pagination import StandardResultsSetPagination


class ContributionList(APIView):
    """
    List all contributions
    """

    def get(self, request):
        """
        Get all contributions
        """
        contributions = Contribution.objects.select_related("member", "window").all()
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(contributions, request, view=self)
        serializer = ContributionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new contribution and credit the unallocated funds pool.
        """
        serializer = ContributionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            unallocated = InvestmentVehicle.objects.select_for_update().get(
                vehicle_type=InvestmentVehicleType.UNALLOCATED
            )
            amount = serializer.validated_data["amount"]

            new_balance = compute_contribution_allocation(
                unallocated.current_value, amount
            )

            unallocated.current_value = new_balance
            unallocated.save(update_fields=["current_value", "updated_at"])

            contribution = serializer.save()

        output = ContributionSerializer(contribution).data
        return Response(output, status=status.HTTP_201_CREATED)
