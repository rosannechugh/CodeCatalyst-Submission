from agent.guardrails import apply_guardrails

def test_guardrails():
    test_cases = [
        {
            "name": "High confidence action",
            "decision": {"action": "REROUTE", "confidence": 0.85}
        },
        {
            "name": "Low confidence action",
            "decision": {"action": "REROUTE", "confidence": 0.5}
        },
        {
            "name": "Repeated action",
            "decision": {"action": "REDUCE_RETRIES", "confidence": 0.9}
        }
    ]

    for case in test_cases:
        print(f"\nTEST: {case['name']}")
        result = apply_guardrails(case["decision"])
        print(result)

if __name__ == "__main__":
    test_guardrails()
