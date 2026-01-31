from agent.decision import score, ACTION_IMPACT


def test_baseline():
    assert score({"success": 0, "latency": 0, "cost": 0, "risk": 0}) == 0


def test_success_beats_latency():
    s = score({"success": 0.2, "latency": 0.3, "cost": 0, "risk": 0})
    assert s > 0


def test_high_risk_penalty():
    risky = score({"success": 0.3, "latency": 0.05, "cost": 0.05, "risk": 0.5})
    safe = score({"success": 0.15, "latency": 0.05, "cost": 0.05, "risk": 0.1})
    assert safe > risky


def test_reroute_beats_retry_delay():
    assert (
        score(ACTION_IMPACT["REROUTE_TRAFFIC"])
        > score(ACTION_IMPACT["INCREASE_RETRY_DELAY"])
    )


def test_suppress_is_bad():
    assert score(ACTION_IMPACT["SUPPRESS_MERCHANT"]) < 0