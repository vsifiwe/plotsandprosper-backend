"""
common/serializers.py
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
        if hasattr(user, "member") and user.member:
            member = user.member
            name = f"{member.firstName} {member.lastName}".strip()
            role = member.role
        data["user"] = {"name": name, "role": role}
        return data
