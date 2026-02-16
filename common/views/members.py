"""
common/views/members.py
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.contrib.auth.models import User
from common.models import Member


DEFAULT_MEMBER_PASSWORD = "Password@123"


class MemberSerializer(serializers.ModelSerializer):
    """
    Member serializer. Creates a Django User when creating a member if user is not provided.
    """

    class Meta:
        """
        Meta class for MemberSerializer
        """

        model = Member
        fields = "__all__"
        extra_kwargs = {"user": {"required": False}}

    def create(self, validated_data):
        """
        Create a new member. Optionally links to an existing user;
        otherwise creates a new User for login.
        """
        user = validated_data.get("user")
        if user is None:
            email = validated_data["email"]
            user, _ = User.objects.get_or_create(
                username=email,
                email=email,
                defaults={},
            )
            if user.password == "" or not user.password.startswith("pbkdf2_"):
                user.set_password(DEFAULT_MEMBER_PASSWORD)
                user.save()
            validated_data["user"] = user
        return super().create(validated_data)


class MemberList(APIView):
    """
    List all members
    """

    def get(self):
        """
        Get all members
        """
        members = Member.objects.all()
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

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
