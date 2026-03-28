"""
Service helpers for common app features.
"""

from decimal import Decimal, ROUND_HALF_UP

from statements.services import get_asset_breakdown, get_portfolio_summary


def get_member_current_value(member):
    """
    Compute the current total portfolio value for a member.
    """
    total = Decimal("0")
    for position in get_asset_breakdown(member):
        if "current_value" in position:
            total += position["current_value"]
        else:
            total += position["total_position_value"]
    return total.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


def build_goal_detail(goal):
    """
    Build goal detail payload including computed progress metrics.
    """

    # use get_portfolio_summary from statements.services to get the current value
    portfolio_summary = get_portfolio_summary(goal.member)
    current_value = portfolio_summary["lifetime"]["amount"]
    target_amount = goal.target_amount

    if target_amount > Decimal("0"):
        progress = ((current_value / target_amount) * Decimal("100")).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )
    else:
        progress = Decimal("0.00")

    gap = max(target_amount - current_value, Decimal("0")).quantize(
        Decimal("0.0001"),
        rounding=ROUND_HALF_UP,
    )

    return {
        "id": goal.id,
        "timeline": goal.timeline,
        "target_amount": goal.target_amount,
        "current_value": current_value,
        "progress_percentage": progress,
        "gap_to_target": gap,
        "created_at": goal.created_at,
        "updated_at": goal.updated_at,
    }


def build_admin_goal_detail(goal):
    """
    Build admin goal payload with member metadata.
    """
    payload = build_goal_detail(goal)
    payload.update(
        {
            "member_id": goal.member.id,
            "member_name": f"{goal.member.firstName} {goal.member.lastName}",
            "member_email": goal.member.email,
        }
    )
    return payload
