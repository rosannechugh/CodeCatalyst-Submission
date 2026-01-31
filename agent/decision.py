from typing import Dict
from payment_analyzer import AnomalyHypothesis


# Impact scores for each possible action
ACTION_IMPACT = {
    "DO_NOTHING": {"success": 0.0, "latency": 0.0, "cost": 0.0, "risk": 0.0},
    "ALERT": {"success": 0.0, "latency": 0.0, "cost": 0.05, "risk": 0.0},
    "INCREASE_RETRY_DELAY": {"success": 0.10, "latency": 0.30, "cost": 0.05, "risk": 0.15},
    "REROUTE_TRAFFIC": {"success": 0.25, "latency": 0.05, "cost": 0.15, "risk": 0.10},
    "SUPPRESS_MERCHANT": {"success": -0.20, "latency": 0.0, "cost": -0.10, "risk": 0.50},
}


def score(impact: Dict[str, float]) -> float:
    """
    Weighted scoring function for decision evaluation
    """
    return (
        impact["success"] * 0.50
        - impact["latency"] * 0.25
        - impact["cost"] * 0.15
        - impact["risk"] * 0.25
    )


def decide_action(hypothesis: AnomalyHypothesis) -> str:
    """
    Decide the best action based on anomaly severity and confidence
    """

    # Low confidence → do nothing
    if hypothesis.confidence < 0.4:
        return "DO_NOTHING"

    # Medium confidence → alert ops
    if 0.4 <= hypothesis.confidence < 0.7:
        return "ALERT"

    # High confidence → evaluate best corrective action
    best_action = "DO_NOTHING"
    best_score = float("-inf")

    for action, impact in ACTION_IMPACT.items():
        s = score(impact)
        if s > best_score:
            best_score = s
            best_action = action

    return best_action
