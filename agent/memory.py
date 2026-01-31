from collections import defaultdict
from datetime import datetime
from typing import Tuple


class AgentMemory:
    """
    Lightweight learning memory for the agent.

    Purpose:
    - Store outcomes of past actions
    - Bias future decisions based on experience
    - Keep learning stable and explainable
    """

    def __init__(self):
        # Key: (anomaly_type, action)
        # Value: success/failure statistics
        self._memory = defaultdict(lambda: {
            "success": 0,
            "failure": 0,
            "last_used": None
        })

    def record_outcome(
        self,
        anomaly_type: str,
        action: str,
        improved: bool
    ) -> None:
        """
        Record the outcome of an action.

        Args:
            anomaly_type: Detected anomaly type (e.g. FAILURE_RATE)
            action: Action taken (e.g. REROUTE_TRAFFIC)
            improved: True if metrics improved after action
        """

        key: Tuple[str, str] = (anomaly_type, action)

        if improved:
            self._memory[key]["success"] += 1
        else:
            self._memory[key]["failure"] += 1

        self._memory[key]["last_used"] = datetime.utcnow()

    def get_action_bias(
        self,
        anomaly_type: str,
        action: str
    ) -> float:
        """
        Return a small confidence bias based on past outcomes.

        Positive bias  -> action worked well before
        Negative bias  -> action often failed
        No history     -> neutral (0.0)
        """

        stats = self._memory.get((anomaly_type, action))
        if not stats:
            return 0.0

        total = stats["success"] + stats["failure"]
        if total == 0:
            return 0.0

        success_rate = stats["success"] / total

        # Gentle scaling to prevent instability
        # Range approximately: [-0.1, +0.1]
        return (success_rate - 0.5) * 0.2

    def snapshot(self):
        """
        Return a read-only snapshot of memory.
        Useful for debugging and explainability.
        """
        return dict(self._memory)

