"""
common/serializers/fund_reallocation_serializer.py
"""

from rest_framework import serializers
from common.models import FundReallocation
from common.serializers.investment_vehicle_serializer import InvestmentVehicleSerializer


class FundReallocationSerializer(serializers.ModelSerializer):
    """
    Fund reallocation serializer with validation.
    """

    source_vehicle_details = InvestmentVehicleSerializer(
        source="source_vehicle", read_only=True
    )
    destination_vehicle_details = InvestmentVehicleSerializer(
        source="destination_vehicle", read_only=True
    )

    class Meta:
        model = FundReallocation
        fields = (
            "id",
            "source_vehicle",
            "destination_vehicle",
            "amount",
            "status",
            "requested_by",
            "reason",
            "created_at",
            "source_vehicle_details",
            "destination_vehicle_details",
        )
        read_only_fields = ("id", "created_at", "status", "requested_by")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate(self, attrs):
        if attrs["source_vehicle"] == attrs["destination_vehicle"]:
            raise serializers.ValidationError(
                {"destination_vehicle": "Source and destination vehicles must be different."}
            )

        source = attrs["source_vehicle"]
        amount = attrs["amount"]
        if amount > source.current_value:
            raise serializers.ValidationError(
                {
                    "amount": (
                        f"Insufficient funds in source vehicle. "
                        f"Available: {source.current_value}, requested: {amount}."
                    )
                }
            )

        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["requested_by"] = {
            "id": str(instance.requested_by.id),
            "full_name": f"{instance.requested_by.firstName} {instance.requested_by.lastName}",
        }
        return data
