import asyncio
import random
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import AsyncGenerator, Optional

@dataclass
class PaymentSignal:
    transaction_id: str
    timestamp: datetime
    amount: float
    currency: str
    status: str
    merchant_id: str
    payment_method: str
    latency_ms: int

async def stream_payment_signals(
    base_delay: float = 1.0, 
    count: Optional[int] = None
) -> AsyncGenerator[PaymentSignal, None]:
    """
    Simulates a live stream of payment signals with temporal correlation.

    Args:
        base_delay: Base time to wait between yielding signals (modified by burst logic).
        count: Number of signals to yield. If None, yields indefinitely.
    """
    generated_count = 0
    
    # State for temporal correlation
    current_amount = 100.0  # Start amount
    is_burst_mode = False   # Traffic state
    burst_probability = 0.3 # Chance to switch states
    
    currencies = ["USD", "EUR", "GBP", "JPY", "AUD", "INR"]
    statuses = ["SUCCESS", "PENDING", "FAILED", "DECLINED"]
    payment_methods = ["CREDIT_CARD", "DEBIT_CARD", "PAYPAL", "APPLE_PAY", "GOOGLE_PAY"]
    
    while count is None or generated_count < count:
        # 1. Temporal Correlation: Traffic Bursts
        # Markov chain-like switching between burst and normal mode
        if random.random() < burst_probability:
            is_burst_mode = not is_burst_mode
            
        if is_burst_mode:
            # Fast signals (high traffic)
            current_delay = random.uniform(0.05, 0.2) * base_delay
        else:
            # Slow signals (normal/low traffic)
            current_delay = random.uniform(0.8, 1.5) * base_delay

        await asyncio.sleep(current_delay)
        
        # 2. Temporal Correlation: Amounts (Random Walk)
        # Change amount by -10% to +10% of current value
        change_factor = random.uniform(0.9, 1.1)
        current_amount *= change_factor
        # Keep amount within reasonable bounds
        current_amount = max(1.0, min(current_amount, 5000.0))
        
        # 3. Simulate System Latency
        # Latency is often log-normally distributed (mostly fast, some long tails)
        latency_ms = int(random.lognormvariate(2, 0.5) * 10) 
        
        signal = PaymentSignal(
            transaction_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            amount=round(current_amount, 2),
            currency=random.choice(currencies),
            status=random.choices(statuses, weights=[0.8, 0.1, 0.05, 0.05])[0],
            merchant_id=f"merch_{random.randint(1000, 9999)}",
            payment_method=random.choice(payment_methods),
            latency_ms=latency_ms
        )
        
        yield signal
        generated_count += 1
