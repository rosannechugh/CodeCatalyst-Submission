# agent/guardrails.py

from datetime import datetime, timedelta

# Internal memory to avoid repeated unsafe actions
_recent_actions = []

def apply_guardrails(decision: dict) -> dict:
    """
    Guardrails sit between decision-making and action execution.
    They ensure the agent acts safely under uncertainty.

    Args:
        decision (dict): Output of decision / trade-off layer.
                         Expected keys: 'action', 'confidence'

    Returns:
        dict: Guardrail-validated decision
    """

    action = decision.get("action")
    confidence = decision.get("confidence", 0.0)

    # -------------------------------------------------
    # Guardrail 1: Confidence Threshold
    # -------------------------------------------------
    if confidence < 0.7:
        decision["action"] = "ALERT"
        decision["guardrail_reason"] = "Low confidence – human review required"
        return decision

    # -------------------------------------------------
    # Guardrail 2: Rate Limiting (avoid action flapping)
    # -------------------------------------------------
    now = datetime.utcnow()
    window = timedelta(minutes=5)

    recent_same_actions = [
        a for a in _recent_actions
        if a["action"] == action and now - a["time"] < window
    ]

    if len(recent_same_actions) >= 2:
        decision["action"] = "ALERT"
        decision["guardrail_reason"] = "Action rate-limited to maintain stability"
        return decision

    # -------------------------------------------------
    # Guardrail 3: Time-bound Autonomous Actions
    # -------------------------------------------------
    decision["ttl_minutes"] = 5  # auto-expire after 5 minutes

    # Record approved action
    _recent_actions.append({
        "action": action,
        "time": now
    })

    decision["guardrail_reason"] = "Passed all guardrails"
    return decision

