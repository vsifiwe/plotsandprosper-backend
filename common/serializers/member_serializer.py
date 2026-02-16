"""
common/serializers/member_serializer.py
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from common.models import Member
from common.constants import DEFAULT_MEMBER_PASSWORD


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
