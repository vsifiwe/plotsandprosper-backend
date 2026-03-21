"""
common/serializers/investment_event_serializer.py
"""

from rest_framework import serializers
from common.models import InvestmentEvent
from common.serializers.investment_vehicle_serializer import InvestmentVehicleSerializer


class InvestmentEventSerializer(serializers.ModelSerializer):
    """
    Investment event serializer with validation.
    """

    investment_vehicle_details = InvestmentVehicleSerializer(
        source="investment_vehicle", read_only=True
    )

    class Meta:
        model = InvestmentEvent
        fields = (
            "id",
            "investment_vehicle",
            "amount",
            "shares",
            "share_price",
            "recorded_by",
            "notes",
            "created_at",
            "investment_vehicle_details",
        )
        read_only_fields = ("id", "created_at")

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_shares(self, value):
        if value <= 0:
            raise serializers.ValidationError("Shares must be greater than zero.")
        return value

    def validate_share_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Share price must be greater than zero.")
        return value

    def validate(self, attrs):
        if attrs["investment_vehicle"].vehicle_type == "UNALLOCATED":
            raise serializers.ValidationError(
                {"investment_vehicle": "Cannot invest into the unallocated funds pool."}
            )

        expected = attrs["shares"] * attrs["share_price"]
        if expected != attrs["amount"]:
            raise serializers.ValidationError(
                {"amount": f"Amount must equal shares * share_price ({expected})."}
            )

        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["recorded_by"] = {
            "id": str(instance.recorded_by.id),
            "full_name": f"{instance.recorded_by.firstName} {instance.recorded_by.lastName}",
        }
        return data
