"""
statements/services.py

Service functions for assembling member investment statement data.
Each function queries the DB and delegates to pure calculation functions.
"""

from decimal import Decimal

from django.db.models import Sum

from common.models import (
    Contribution,
    InvestmentVehicle,
    InvestmentVehicleType,
    MemberShareAllocation,
    NAVRecord,
    AssetOwnershipRecord,
)
from calculations.statement import (
    compute_share_position,
    compute_asset_position,
)

SHARE_BASED_TYPES = {
    InvestmentVehicleType.SHARES,
    InvestmentVehicleType.SAVINGS_ACCOUNT,
    InvestmentVehicleType.GOVERNMENT_BOND,
}

ASSET_BASED_TYPES = {
    InvestmentVehicleType.LAND,
    InvestmentVehicleType.OTHER,
}


def _get_member_share_positions(member):
    """
    Get all share-based positions for a member.
    Returns list of dicts with vehicle info and computed position metrics.
    """
    positions = []

    vehicle_aggregates = (
        MemberShareAllocation.objects.filter(member=member)
        .values("investment_vehicle__id", "investment_vehicle__name", "investment_vehicle__vehicle_type")
        .annotate(
            total_shares=Sum("shares"),
            total_book_value=Sum("amount"),
        )
    )

    for agg in vehicle_aggregates:
        vehicle_type = agg["investment_vehicle__vehicle_type"]
        if vehicle_type not in SHARE_BASED_TYPES:
            continue

        total_shares = agg["total_shares"] or Decimal("0")
        if total_shares <= Decimal("0"):
            continue

        latest_nav = (
            NAVRecord.objects.filter(investment_vehicle_id=agg["investment_vehicle__id"])
            .order_by("-recorded_at")
            .values_list("nav_per_share", flat=True)
            .first()
        )

        if latest_nav is None:
            continue

        position = compute_share_position(
            total_shares=total_shares,
            book_value=agg["total_book_value"] or Decimal("0"),
            current_nav=latest_nav,
        )
        position["vehicle_id"] = agg["investment_vehicle__id"]
        position["vehicle_name"] = agg["investment_vehicle__name"]
        positions.append(position)

    return positions


def _get_member_asset_positions(member):
    """
    Get all asset-based positions for a member.
    Returns list of dicts with vehicle info and computed position metrics.
    """
    positions = []

    vehicle_ids = (
        AssetOwnershipRecord.objects.filter(member=member)
        .values_list("investment_vehicle_id", flat=True)
        .distinct()
    )

    for vehicle_id in vehicle_ids:
        latest_record = (
            AssetOwnershipRecord.objects.filter(
                member=member, investment_vehicle_id=vehicle_id
            )
            .select_related("investment_vehicle")
            .order_by("-recorded_at")
            .first()
        )

        if latest_record is None:
            continue

        vehicle = latest_record.investment_vehicle
        if vehicle.vehicle_type not in ASSET_BASED_TYPES:
            continue

        position = compute_asset_position(
            ownership_percentage=latest_record.ownership_percentage,
            equity_value=latest_record.equity_value,
            cash_distributed=latest_record.cash_distributed,
            cash_pending=latest_record.cash_pending,
            total_cost_basis=latest_record.equity_value,
        )
        position["vehicle_id"] = vehicle.id
        position["vehicle_name"] = vehicle.name
        positions.append(position)

    return positions


def get_portfolio_summary(member):
    """
    Assemble portfolio summary for a member.
    Returns dict with lifetime, group, membership, and investment metrics.
    """
    from common.models import Member
    from common.models.member import MemberStatus

    # Personal lifetime contributions
    lifetime_contributions = (
        Contribution.objects.filter(member=member).aggregate(
            total=Sum("amount")
        )["total"]
        or Decimal("0")
    )

    # Group-wide total contributions
    group_total = (
        Contribution.objects.aggregate(total=Sum("amount"))["total"]
        or Decimal("0")
    )

    # Active members count
    active_members = Member.objects.filter(status=MemberStatus.ACTIVE).count()

    # Total investment vehicles held by the group (excluding unallocated)
    total_investments = InvestmentVehicle.objects.exclude(
        vehicle_type=InvestmentVehicleType.UNALLOCATED
    ).count()

    return {
        "lifetime": {
            "amount": lifetime_contributions,
            "growth": Decimal("0.01"),
        },
        "group": {
            "amount": group_total,
            "growth": Decimal("1"),
        },
        "membership": {
            "amount": Decimal(active_members),
            "growth": Decimal("0.1"),
        },
        "investment": {
            "amount": Decimal(total_investments),
            "growth": Decimal("0.1"),
        },
    }


def get_investment_vehicles():
    """
    Return all investment vehicles excluding unallocated funds.
    """
    return list(
        InvestmentVehicle.objects.exclude(
            vehicle_type=InvestmentVehicleType.UNALLOCATED
        ).values("id", "name", "vehicle_type", "current_value", "description")
    )


def get_asset_breakdown(member):
    """
    Assemble asset breakdown for a member.
    Returns list of position dicts (share-based and asset-based).
    """
    share_positions = _get_member_share_positions(member)
    asset_positions = _get_member_asset_positions(member)
    return share_positions + asset_positions


def get_transaction_history(member, page=1, page_size=20):
    """
    Assemble paginated transaction history for a member.
    Merges contributions and share allocations, ordered by date descending.
    Returns dict with count, results, and pagination info.
    """
    transactions = []

    contributions = Contribution.objects.filter(member=member).values(
        "recorded_at", "amount", "window__name"
    )
    for c in contributions:
        transactions.append({
            "date": c["recorded_at"],
            "description": f"{c['window__name']} Contribution",
            "amount": c["amount"],
            "type": "CONTRIBUTION",
        })

    allocations = (
        MemberShareAllocation.objects.filter(member=member)
        .select_related("investment_vehicle")
        .values("recorded_at", "amount", "shares", "share_price", "investment_vehicle__name", "notes")
    )
    for a in allocations:
        if a["amount"] < Decimal("0"):
            description = f"Shares Withdrawn (NAV {a['share_price']})"
        else:
            description = a["notes"] if a["notes"] else f"{a['investment_vehicle__name']} Allocation"
        transactions.append({
            "date": a["recorded_at"],
            "description": description,
            "amount": a["amount"],
            "type": "SHARE_ALLOCATION",
        })

    transactions.sort(key=lambda t: t["date"])

    cumulative = Decimal("0")
    for tx in transactions:
        cumulative += tx["amount"]
        tx["cumulative_contributions"] = cumulative

    transactions.reverse()

    total_count = len(transactions)
    start = (page - 1) * page_size
    end = start + page_size
    page_results = transactions[start:end]

    return {
        "count": total_count,
        "page": page,
        "page_size": page_size,
        "results": page_results,
    }
