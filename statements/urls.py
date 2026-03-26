"""
statements/urls.py
"""

from django.urls import path

from statements.views import (
    PortfolioSummaryView,
    AssetBreakdownView,
    InvestmentVehicleListView,
    TransactionHistoryView,
)

urlpatterns = [
    path("summary/", PortfolioSummaryView.as_view(), name="portfolio_summary"),
    path("assets/", AssetBreakdownView.as_view(), name="asset_breakdown"),
    path("investments/", InvestmentVehicleListView.as_view(), name="investment_vehicles"),
    path("transactions/", TransactionHistoryView.as_view(), name="transaction_history"),
]
