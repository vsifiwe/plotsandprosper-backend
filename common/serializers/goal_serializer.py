"""
Serializers for member goals.
"""

from rest_framework import serializers

from common.models import Goal


class GoalSerializer(serializers.ModelSerializer):
    """
    Serializer for create/update goal operations.
    """

    class Meta:
        model = Goal
        fields = ["id", "timeline", "target_amount", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class GoalDetailSerializer(serializers.Serializer):
    """
    Read serializer for member goal details with computed metrics.
    """

    id = serializers.IntegerField()
    timeline = serializers.CharField()
    target_amount = serializers.DecimalField(max_digits=20, decimal_places=4)
    current_value = serializers.DecimalField(max_digits=20, decimal_places=4)
    progress_percentage = serializers.DecimalField(max_digits=7, decimal_places=2)
    gap_to_target = serializers.DecimalField(max_digits=20, decimal_places=4)
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()


class AdminGoalListSerializer(GoalDetailSerializer):
    """
    Read serializer for admin goal listing.
    """

    member_id = serializers.UUIDField()
    member_name = serializers.CharField()
    member_email = serializers.EmailField()
