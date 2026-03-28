"""
Views for member and admin goal management.
"""

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Goal, MemberRole
from common.pagination import StandardResultsSetPagination
from common.serializers import (
    AdminGoalListSerializer,
    GoalDetailSerializer,
    GoalSerializer,
)
from common.services import build_goal_detail, build_admin_goal_detail


class MemberGoalView(APIView):
    """
    Manage the authenticated member's single goal.
    """

    def get(self, request):
        """
        Get the authenticated member's goal.
        """
        goal = get_object_or_404(Goal, member=request.user.member)
        serializer = GoalDetailSerializer(build_goal_detail(goal))
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new goal for the authenticated member.
        """
        member = request.user.member
        if hasattr(member, "goal"):
            return Response(
                {"detail": "Member already has an active goal."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = GoalSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        goal = serializer.save(member=member)
        output = GoalDetailSerializer(build_goal_detail(goal))
        return Response(output.data, status=status.HTTP_201_CREATED)

    def patch(self, request):
        """
        Update the authenticated member's goal.
        """
        return self._update(request, partial=True)

    def put(self, request):
        """
        Update the authenticated member's goal.
        """
        return self._update(request, partial=False)

    def delete(self, request):
        """
        Delete the authenticated member's goal.
        """
        goal = get_object_or_404(Goal, member=request.user.member)
        goal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def _update(self, request, partial):
        """
        Update the authenticated member's goal.
        """
        goal = get_object_or_404(Goal, member=request.user.member)
        serializer = GoalSerializer(goal, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        goal = serializer.save()
        output = GoalDetailSerializer(build_goal_detail(goal))
        return Response(output.data)


class AdminGoalListView(APIView):
    """
    List all member goals for admins.
    """

    def get(self, request):
        """
        List all member goals for admins.
        """
        member = request.user.member
        if member.role != MemberRole.ADMIN:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )

        goals = Goal.objects.select_related("member").all()
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(goals, request, view=self)
        serializer = AdminGoalListSerializer(
            [build_admin_goal_detail(goal) for goal in page],
            many=True,
        )
        return paginator.get_paginated_response(serializer.data)
