"""
common/views/investment_events.py
"""

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from calculations.investment import compute_investment_balances
from common.models import InvestmentEvent, InvestmentVehicle, InvestmentVehicleType
from common.serializers import InvestmentEventSerializer
from common.pagination import StandardResultsSetPagination


class InvestmentEventList(APIView):
    """
    List all investment events or create a new one (invest from unallocated pool).
    """

    def get(self, request):
        """
        List investment events. Optional ?vehicle=<id> filter for per-vehicle history.
        """
        events = InvestmentEvent.objects.select_related(
            "investment_vehicle", "recorded_by"
        ).all()

        vehicle_id = request.query_params.get("vehicle")
        if vehicle_id:
            events = events.filter(investment_vehicle_id=vehicle_id)

        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(events, request, view=self)
        serializer = InvestmentEventSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new investment event: move funds from unallocated pool to a vehicle.
        """
        serializer = InvestmentEventSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            unallocated = InvestmentVehicle.objects.select_for_update().get(
                vehicle_type=InvestmentVehicleType.UNALLOCATED
            )
            vehicle = InvestmentVehicle.objects.select_for_update().get(
                pk=serializer.validated_data["investment_vehicle"].pk
            )

            shares = serializer.validated_data["shares"]
            share_price = serializer.validated_data["share_price"]

            _amount, new_unallocated, new_vehicle = compute_investment_balances(
                unallocated.current_value,
                vehicle.current_value,
                shares,
                share_price,
            )

            unallocated.current_value = new_unallocated
            unallocated.save(update_fields=["current_value", "updated_at"])

            vehicle.current_value = new_vehicle
            vehicle.save(update_fields=["current_value", "updated_at"])

            event = serializer.save(recorded_by=request.user.member)

        output = InvestmentEventSerializer(event).data
        return Response(output, status=status.HTTP_201_CREATED)
