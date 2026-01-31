import asyncio
from payment_generator import stream_payment_signals
from payment_analyzer import PaymentAnalyzer

async def main():
    analyzer = PaymentAnalyzer(window_size=30)
    print("Starting Live Payment Analysis...")
    print("Watching for patterns (High Latency, Failure Spikes, Merchant Outages)...")
    print("-" * 60)
    
    try:
        # Stream 50 signals
        async for signal in stream_payment_signals(base_delay=0.3, count=200):
            # 1. Print simple log
            status_icon = "[OK]" if signal.status == "SUCCESS" else "[X] "
            print(f"{status_icon} {signal.currency} {signal.amount:6.2f} | {signal.latency_ms}ms")
            
            # 2. Analyze
            hypothesis = analyzer.add_signal(signal)
            
            # 3. Report findings
            if hypothesis:
                print(f"\n   >>> INSIGHT GENERATED [{hypothesis.severity}]")
                print(f"   TYPE: {hypothesis.type}")
                print(f"   WHAT: {hypothesis.description}")
                print(f"   WHY : {hypothesis.root_cause_guess}")
                print(f"   CONF: {hypothesis.confidence * 100:.0f}%\n")
                
    except KeyboardInterrupt:
        print("\nAnalysis stopped.")

if __name__ == "__main__":
    asyncio.run(main())
