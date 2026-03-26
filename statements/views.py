"""
statements/views.py

API views for member investment statement endpoints.
"""

from rest_framework.response import Response
from rest_framework.views import APIView

from statements.serializers import (
    PortfolioSummarySerializer,
    SharePositionSerializer,
    AssetPositionSerializer,
    InvestmentVehicleListSerializer,
    TransactionHistoryResponseSerializer,
)
from statements.services import (
    get_portfolio_summary,
    get_asset_breakdown,
    get_investment_vehicles,
    get_transaction_history,
)


class PortfolioSummaryView(APIView):
    """
    GET /api/v1/members/me/statement/summary/

    Returns portfolio summary for the authenticated member.
    """

    def get(self, request):
        member = request.user.member
        data = get_portfolio_summary(member)
        serializer = PortfolioSummarySerializer(data)
        return Response(serializer.data)


class AssetBreakdownView(APIView):
    """
    GET /api/v1/members/me/statement/assets/

    Returns asset breakdown for the authenticated member.
    """

    def get(self, request):
        member = request.user.member
        positions = get_asset_breakdown(member)

        results = []
        for pos in positions:
            if "shares_owned" in pos:
                serializer = SharePositionSerializer(pos)
            else:
                serializer = AssetPositionSerializer(pos)
            results.append(serializer.data)

        return Response(results)


class InvestmentVehicleListView(APIView):
    """
    GET /api/v1/members/me/statement/investments/

    Returns list of investment vehicles held by the group.
    """

    def get(self, request):
        data = get_investment_vehicles()
        serializer = InvestmentVehicleListSerializer(data, many=True)
        return Response(serializer.data)


class TransactionHistoryView(APIView):
    """
    GET /api/v1/members/me/statement/transactions/

    Returns paginated transaction history for the authenticated member.
    """

    def get(self, request):
        member = request.user.member
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))

        data = get_transaction_history(member, page=page, page_size=page_size)
        serializer = TransactionHistoryResponseSerializer(data)
        return Response(serializer.data)
