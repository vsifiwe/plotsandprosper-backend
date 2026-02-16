"""
common/models/member.py
"""

import uuid

from django.db import models
from django.contrib.auth.models import User


class MemberStatus(models.TextChoices):
    """
    Member status choices
    """

    ACTIVE = "ACTIVE", "Active"
    EXITED = "EXITED", "Exited"
    SUSPENDED = "SUSPENDED", "Suspended"


class MemberRole(models.TextChoices):
    """
    Member role choices
    """

    MEMBER = "MEMBER", "Member"
    ADMIN = "ADMIN", "Admin"
    AUDITOR = "AUDITOR", "Auditor"


class Member(models.Model):
    """
    Member model
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=32, unique=True)
    nationalId = models.CharField(max_length=16, unique=True)
    status = models.CharField(
        max_length=16, choices=MemberStatus.choices, default=MemberStatus.ACTIVE
    )
    joinDate = models.DateField()
    role = models.CharField(
        max_length=16, choices=MemberRole.choices, default=MemberRole.MEMBER
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="member"
    )

    def __str__(self):
        """
        String representation of the member
        """
        return f"{self.firstName} {self.lastName}"
