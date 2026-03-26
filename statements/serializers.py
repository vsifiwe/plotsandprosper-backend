"""
statements/serializers.py

Read-only serializers for member investment statement endpoints.
"""

from rest_framework import serializers


class MemberInfoSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    status = serializers.CharField()
    join_date = serializers.DateField(allow_null=True)


class SummaryMetricSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=20, decimal_places=4)
    growth = serializers.DecimalField(max_digits=10, decimal_places=4)


class PortfolioSummarySerializer(serializers.Serializer):
    lifetime = SummaryMetricSerializer()
    group = SummaryMetricSerializer()
    membership = SummaryMetricSerializer()
    investment = SummaryMetricSerializer()


class SharePositionSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()
    vehicle_name = serializers.CharField()
    shares_owned = serializers.DecimalField(max_digits=20, decimal_places=4)
    book_value = serializers.DecimalField(max_digits=20, decimal_places=4)
    average_entry_nav = serializers.DecimalField(max_digits=20, decimal_places=2)
    current_nav = serializers.DecimalField(max_digits=20, decimal_places=4)
    current_value = serializers.DecimalField(max_digits=20, decimal_places=2)
    unrealized_gain_loss = serializers.DecimalField(max_digits=20, decimal_places=2)
    return_percentage = serializers.DecimalField(max_digits=10, decimal_places=2)


class AssetPositionSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()
    vehicle_name = serializers.CharField()
    ownership_percentage = serializers.DecimalField(max_digits=10, decimal_places=4)
    current_equity = serializers.DecimalField(max_digits=20, decimal_places=4)
    unrealized_value = serializers.DecimalField(max_digits=20, decimal_places=4)
    cash_distributed = serializers.DecimalField(max_digits=20, decimal_places=4)
    cash_pending = serializers.DecimalField(max_digits=20, decimal_places=4)
    realized_gain = serializers.DecimalField(max_digits=20, decimal_places=4)
    total_position_value = serializers.DecimalField(max_digits=20, decimal_places=4)
    total_return_percentage = serializers.DecimalField(max_digits=10, decimal_places=2)


class InvestmentVehicleListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    vehicle_type = serializers.CharField()
    current_value = serializers.DecimalField(max_digits=20, decimal_places=4)
    description = serializers.CharField()


class TransactionHistoryItemSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    description = serializers.CharField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=4)
    cumulative_contributions = serializers.DecimalField(max_digits=20, decimal_places=4)
    type = serializers.CharField()


class TransactionHistoryResponseSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    results = TransactionHistoryItemSerializer(many=True)
