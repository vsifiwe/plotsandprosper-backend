"""
common/admin.py
"""

from django.contrib import admin
from common.models import Member, ContributionWindow, Contribution


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """
    Member admin
    """

    list_display = [
        "firstName",
        "lastName",
        "email",
        "phone",
        "nationalId",
        "status",
        "joinDate",
        "role",
    ]
    list_filter = ["status", "role"]
    search_fields = ["firstName", "lastName", "email", "phone", "nationalId"]
    list_per_page = 10


@admin.register(ContributionWindow)
class ContributionWindowAdmin(admin.ModelAdmin):
    """
    Contribution window admin
    """

    list_display = ["name", "start_at", "end_at"]
    list_filter = ["start_at", "end_at"]
    search_fields = ["name"]
    list_per_page = 10


@admin.register(Contribution)
class ContributionAdmin(admin.ModelAdmin):
    """
    Contribution admin
    """

    list_display = ["member", "window", "amount", "recorded_at"]
    list_filter = ["member", "window", "recorded_at"]
    search_fields = ["member__firstName", "member__lastName", "window__name"]
    list_per_page = 10
