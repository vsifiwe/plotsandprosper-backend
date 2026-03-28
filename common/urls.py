"""
common/urls.py
"""

from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView
from common.views import (
    MemberList,
    CustomTokenObtainPairView,
    ContributionWindowList,
    ContributionList,
    InvestmentVehicleList,
    GroupAnalyticsView,
    FundReallocationList,
    InvestmentEventList,
    MemberGoalView,
    AdminGoalListView,
)


urlpatterns = [
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("members/", MemberList.as_view(), name="member_list"),
    path(
        "contribution-windows/",
        ContributionWindowList.as_view(),
        name="contribution_window_list",
    ),
    path("contributions/", ContributionList.as_view(), name="contribution_list"),
    path(
        "investment-accounts/",
        InvestmentVehicleList.as_view(),
        name="investment_account_list",
    ),
    path(
        "fund-reallocations/",
        FundReallocationList.as_view(),
        name="fund_reallocation_list",
    ),
    path(
        "investment-events/",
        InvestmentEventList.as_view(),
        name="investment_event_list",
    ),
    path("analytics/", GroupAnalyticsView.as_view(), name="group_analytics"),
    path("members/me/goal/", MemberGoalView.as_view(), name="member_goal"),
    path("admin/goals/", AdminGoalListView.as_view(), name="admin_goal_list"),
    path("members/me/statement/", include("statements.urls")),
]
