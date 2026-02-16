"""
common/views/members.py
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from common.models.member import Member

class MemberSerializer(serializers.ModelSerializer):
    """
    Member serializer
    """
    class Meta:
        """
        Meta class
        """
        model = Member
        fields = "__all__"

class MemberList(APIView):
    """
    List all members
    """
    def get(self, request):
        """
        Get all members
        """
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)
    def post(self, request):
        """
        Create a new member
        """
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)