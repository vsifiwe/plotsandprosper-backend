"""
common/views/fund_reallocations.py
"""

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from calculations.reallocation import compute_reallocation_balances
from common.models import FundReallocation, InvestmentVehicle
from common.serializers import FundReallocationSerializer
from common.pagination import StandardResultsSetPagination


class FundReallocationList(APIView):
    """
    List all fund reallocations or create a new one.
    """

    def get(self, request):
        """
        Get all fund reallocations.
        """
        reallocations = FundReallocation.objects.select_related(
            "source_vehicle", "destination_vehicle", "requested_by"
        ).all()
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(reallocations, request, view=self)
        serializer = FundReallocationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new fund reallocation and update vehicle balances atomically.
        """
        serializer = FundReallocationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Lock both vehicles to prevent concurrent balance changes
            source = InvestmentVehicle.objects.select_for_update().get(
                pk=serializer.validated_data["source_vehicle"].pk
            )
            destination = InvestmentVehicle.objects.select_for_update().get(
                pk=serializer.validated_data["destination_vehicle"].pk
            )
            amount = serializer.validated_data["amount"]

            new_source_value, new_destination_value = compute_reallocation_balances(
                source.current_value, destination.current_value, amount
            )

            source.current_value = new_source_value
            source.save(update_fields=["current_value", "updated_at"])

            destination.current_value = new_destination_value
            destination.save(update_fields=["current_value", "updated_at"])

            reallocation = serializer.save()

        # Re-serialize with updated vehicle details
        output = FundReallocationSerializer(reallocation).data
        return Response(output, status=status.HTTP_201_CREATED)
