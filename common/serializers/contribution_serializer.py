"""
common/serializers/contribution_serializer.py
"""

from rest_framework import serializers
from common.models import Contribution
from common.serializers.contribution_window_serializer import (
    ContributionWindowSerializer,
)


class ContributionSerializer(serializers.ModelSerializer):
    """
    Contribution serializer
    """

    window_details = ContributionWindowSerializer(source="window", read_only=True)

    class Meta:
        """
        Meta class for ContributionSerializer
        """

        model = Contribution
        fields = (
            "id",
            "member",
            "window",
            "amount",
            "recorded_at",
            "created_at",
            "window_details",
        )
        read_only_fields = ("id", "created_at", "window_details")

    def create(self, validated_data):
        """
        Create a new contribution
        """
        return Contribution.objects.create(**validated_data)

    def to_representation(self, instance):
        """
        Return minimal member data for the `member` field in API responses.
        """
        data = super().to_representation(instance)
        data["member"] = {
            "id": str(instance.member.id),
            "full_name": f"{instance.member.firstName} {instance.member.lastName}",
        }
        return data
