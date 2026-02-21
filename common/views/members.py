"""
common/views/members.py
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common.models import Member
from common.serializers import MemberSerializer
from common.pagination import StandardResultsSetPagination


class MemberList(APIView):
    """
    List all members
    """

    def get(self, request):
        """
        Get all members
        """
        members = Member.objects.all().order_by("-createdAt")
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(members, request, view=self)
        serializer = MemberSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        """
        Create a new member. Optionally links to an existing user;
        otherwise creates a new User for login.
        """
        serializer = MemberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
