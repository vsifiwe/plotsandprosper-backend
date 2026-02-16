"""
common/views/contribution.py
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.models import Contribution

from common.serializers import ContributionSerializer


class ContributionList(APIView):
    """
    List all contributions
    """

    def get(self, request):
        """
        Get all contributions
        """
        contributions = Contribution.objects.all()
        serializer = ContributionSerializer(contributions, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new contribution
        """
        serializer = ContributionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
