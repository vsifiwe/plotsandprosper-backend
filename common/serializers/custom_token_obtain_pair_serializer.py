"""
common/serializers/custom_token_obtain_pair_serializer.py
"""

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Adds user name and role to the token response.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        name = ""
        role = None
        email = ""
        if hasattr(user, "member") and user.member:
            member = user.member
            name = f"{member.firstName} {member.lastName}".strip()
            role = member.role
            email = member.email
        data["user"] = {"name": name, "role": role, "email": email}
        return data
