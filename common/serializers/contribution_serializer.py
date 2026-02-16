"""
common/serializers/contribution_serializer.py
"""

from rest_framework import serializers
from common.models import Contribution


class ContributionSerializer(serializers.ModelSerializer):
    """
    Contribution serializer
    """

    class Meta:
        """
        Meta class for ContributionSerializer
        """

        model = Contribution
        fields = "__all__"

    def create(self, validated_data):
        """
        Create a new contribution
        """
        return Contribution.objects.create(**validated_data)
