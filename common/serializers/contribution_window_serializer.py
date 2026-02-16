"""
common/serializers/contribution_window_serializer.py
"""

from rest_framework import serializers
from common.models import ContributionWindow


class ContributionWindowSerializer(serializers.ModelSerializer):
    """
    Contribution window serializer.
    """

    class Meta:
        """
        Meta class for ContributionWindowSerializer
        """

        model = ContributionWindow
        fields = "__all__"
