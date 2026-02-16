"""
common/views/auth.py
"""

from rest_framework_simplejwt.views import TokenObtainPairView
from common.serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
