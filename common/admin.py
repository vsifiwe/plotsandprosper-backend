"""
common/admin.py
"""
from django.contrib import admin
from common.models import Member


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
