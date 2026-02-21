"""
common/views/contribution_windows.py
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.models import ContributionWindow
from common.serializers import ContributionWindowSerializer
from common.pagination import StandardResultsSetPagination


class ContributionWindowList(APIView):
    """
    List all contribution windows
    """

    def get(self, request):
        """
        Get all contribution windows
        """
        contribution_windows = ContributionWindow.objects.all()
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(contribution_windows, request, view=self)
        serializer = ContributionWindowSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new contribution window
        """
        serializer = ContributionWindowSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
