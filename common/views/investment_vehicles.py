"""
common/views/investment_vehicles.py
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.models import InvestmentVehicle
from common.serializers import InvestmentVehicleSerializer
from common.pagination import StandardResultsSetPagination


class InvestmentVehicleList(APIView):
    """
    List all investment vehicles.
    """

    def get(self, request):
        """
        Get all investment vehicles.
        """
        investment_vehicles = InvestmentVehicle.objects.all()
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(investment_vehicles, request, view=self)
        serializer = InvestmentVehicleSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new investment vehicle.
        """
        serializer = InvestmentVehicleSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
