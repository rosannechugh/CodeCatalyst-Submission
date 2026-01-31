from agent.memory import AgentMemory


def test_agent_memory():
    memory = AgentMemory()

    anomaly_type = "FAILURE_RATE"
    action = "REROUTE_TRAFFIC"

    print("=== Initial Bias (no history) ===")
    print(memory.get_action_bias(anomaly_type, action))  # Expected: 0.0

    print("\n=== Recording Successful Outcomes ===")
    memory.record_outcome(anomaly_type, action, improved=True)
    memory.record_outcome(anomaly_type, action, improved=True)
    memory.record_outcome(anomaly_type, action, improved=True)

    print("Bias after successes:")
    print(memory.get_action_bias(anomaly_type, action))  # Expected: positive value

    print("\n=== Recording a Failure ===")
    memory.record_outcome(anomaly_type, action, improved=False)

    print("Bias after one failure:")
    print(memory.get_action_bias(anomaly_type, action))  # Expected: smaller positive value

    print("\n=== Different Action, No History ===")
    print(memory.get_action_bias("LATENCY", "INCREASE_RETRY_DELAY"))  # Expected: 0.0


if __name__ == "__main__":
    test_agent_memory()
