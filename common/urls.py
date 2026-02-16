"""
common/urls.py
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from common.views import MemberList, CustomTokenObtainPairView

urlpatterns = [
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("members/", MemberList.as_view(), name="member_list"),
]
