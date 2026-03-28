from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from common.models import (
    AssetOwnershipRecord,
    Goal,
    GoalTimeline,
    InvestmentVehicle,
    InvestmentVehicleType,
    Member,
    MemberRole,
    MemberShareAllocation,
    NAVRecord,
)


class GoalModelTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="member@example.com", password="password"
        )
        self.member = Member.objects.create(
            firstName="Member",
            lastName="User",
            email="member@example.com",
            phone="0780000001",
            nationalId="1199900000000001",
            joinDate=timezone.now().date(),
            user=self.user,
        )

    def test_member_can_only_have_one_goal(self):
        Goal.objects.create(
            member=self.member,
            timeline=GoalTimeline.ONE_YEAR,
            target_amount=Decimal("1000.0000"),
        )

        with self.assertRaises(IntegrityError):
            Goal.objects.create(
                member=self.member,
                timeline=GoalTimeline.TWO_YEARS,
                target_amount=Decimal("2000.0000"),
            )

    def test_target_amount_must_be_positive(self):
        goal = Goal(
            member=self.member,
            timeline=GoalTimeline.ONE_YEAR,
            target_amount=Decimal("0.0000"),
        )

        with self.assertRaises(ValidationError):
            goal.full_clean()


class MemberGoalApiTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="member2@example.com", password="password"
        )
        self.member = Member.objects.create(
            firstName="Jane",
            lastName="Doe",
            email="member2@example.com",
            phone="0780000002",
            nationalId="1199900000000002",
            joinDate=timezone.now().date(),
            user=self.user,
        )
        self.client.force_authenticate(self.user)
        self.url = reverse("member_goal")

    def test_create_and_retrieve_goal_with_progress_metrics(self):
        vehicle = InvestmentVehicle.objects.create(
            name="Growth Fund",
            vehicle_type=InvestmentVehicleType.SHARES,
            current_value=Decimal("0.0000"),
        )
        MemberShareAllocation.objects.create(
            member=self.member,
            investment_vehicle=vehicle,
            shares=Decimal("10.0000"),
            share_price=Decimal("100.0000"),
            amount=Decimal("1000.0000"),
            recorded_at=timezone.now(),
        )
        NAVRecord.objects.create(
            investment_vehicle=vehicle,
            nav_per_share=Decimal("150.0000"),
            recorded_at=timezone.now(),
        )

        response = self.client.post(
            self.url,
            {"timeline": GoalTimeline.ONE_YEAR, "target_amount": "2000.0000"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Decimal(response.data["current_value"]), Decimal("1500.0000"))
        self.assertEqual(Decimal(response.data["progress_percentage"]), Decimal("75.00"))
        self.assertEqual(Decimal(response.data["gap_to_target"]), Decimal("500.0000"))

        get_response = self.client.get(self.url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["timeline"], GoalTimeline.ONE_YEAR)

    def test_duplicate_goal_creation_is_rejected(self):
        Goal.objects.create(
            member=self.member,
            timeline=GoalTimeline.ONE_YEAR,
            target_amount=Decimal("1000.0000"),
        )

        response = self.client.post(
            self.url,
            {"timeline": GoalTimeline.TWO_YEARS, "target_amount": "3000.0000"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_member_can_update_and_delete_goal(self):
        Goal.objects.create(
            member=self.member,
            timeline=GoalTimeline.ONE_YEAR,
            target_amount=Decimal("1000.0000"),
        )

        patch_response = self.client.patch(
            self.url,
            {"timeline": GoalTimeline.FIVE_YEARS, "target_amount": "2500.0000"},
            format="json",
        )
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_response.data["timeline"], GoalTimeline.FIVE_YEARS)
        self.assertEqual(Decimal(patch_response.data["target_amount"]), Decimal("2500.0000"))

        delete_response = self.client.delete(self.url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Goal.objects.filter(member=self.member).exists())

    def test_progress_can_exceed_one_hundred_percent(self):
        vehicle = InvestmentVehicle.objects.create(
            name="Land Position",
            vehicle_type=InvestmentVehicleType.LAND,
            current_value=Decimal("0.0000"),
        )
        AssetOwnershipRecord.objects.create(
            member=self.member,
            investment_vehicle=vehicle,
            ownership_percentage=Decimal("50.0000"),
            equity_value=Decimal("5000.0000"),
            cash_distributed=Decimal("0.0000"),
            cash_pending=Decimal("0.0000"),
            recorded_at=timezone.now(),
        )
        Goal.objects.create(
            member=self.member,
            timeline=GoalTimeline.TWO_YEARS,
            target_amount=Decimal("2000.0000"),
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Decimal(response.data["progress_percentage"]), Decimal("250.00"))
        self.assertEqual(Decimal(response.data["gap_to_target"]), Decimal("0.0000"))


class AdminGoalApiTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="admin@example.com", password="password"
        )
        self.admin_member = Member.objects.create(
            firstName="Admin",
            lastName="User",
            email="admin@example.com",
            phone="0780000003",
            nationalId="1199900000000003",
            joinDate=timezone.now().date(),
            role=MemberRole.ADMIN,
            user=self.admin_user,
        )
        self.regular_user = User.objects.create_user(
            username="user@example.com", password="password"
        )
        self.regular_member = Member.objects.create(
            firstName="Regular",
            lastName="User",
            email="user@example.com",
            phone="0780000004",
            nationalId="1199900000000004",
            joinDate=timezone.now().date(),
            user=self.regular_user,
        )
        Goal.objects.create(
            member=self.regular_member,
            timeline=GoalTimeline.TEN_YEARS,
            target_amount=Decimal("10000.0000"),
        )
        self.url = reverse("admin_goal_list")

    def test_admin_can_list_all_goals(self):
        self.client.force_authenticate(self.admin_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["member_email"], "user@example.com")

    def test_non_admin_cannot_list_all_goals(self):
        self.client.force_authenticate(self.regular_user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
