"""
common/serializers/investment_vehicle_serializer.py
"""

from rest_framework import serializers
from common.models import InvestmentVehicle


class InvestmentVehicleSerializer(serializers.ModelSerializer):
    """
    Investment vehicle serializer.
    """

    class Meta:
        """
        Meta class for InvestmentVehicleSerializer.
        """

        model = InvestmentVehicle
        fields = "__all__"

    def validate_vehicle_type(self, value):
        if value == "UNALLOCATED":
            raise serializers.ValidationError(
                "Cannot manually create an unallocated funds vehicle."
            )
        return value
