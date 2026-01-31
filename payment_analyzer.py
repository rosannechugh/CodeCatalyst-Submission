from collections import deque, Counter
from dataclasses import dataclass
from typing import List, Optional
from payment_generator import PaymentSignal

@dataclass
class AnomalyHypothesis:
    type: str  # "LATENCY", "FAILURE_RATE", "TRAFFIC_SPIKE"
    severity: str # "INFO", "WARNING", "CRITICAL"
    description: str
    root_cause_guess: str
    confidence: float

class PaymentAnalyzer:
    def __init__(self, window_size: int = 20):
        self.window_size = window_size
        self.history: deque[PaymentSignal] = deque(maxlen=window_size)
        
    def add_signal(self, signal: PaymentSignal) -> Optional[AnomalyHypothesis]:
        self.history.append(signal)
        if len(self.history) < 10: # Need some data
            return None
        return self._analyze()

    def _analyze(self) -> Optional[AnomalyHypothesis]:
        signals = list(self.history)
        
        # Metrics
        failures = [s for s in signals if s.status in ("FAILED", "DECLINED")]
        avg_latency = sum(s.latency_ms for s in signals) / len(signals)
        failure_rate = len(failures) / len(signals)
        
        # 1. High Failure Rate Detection
        if failure_rate > 0.25: # > 25% failure
            # Root Cause Analysis
            failed_merchants = [s.merchant_id for s in failures]
            failed_currencies = [s.currency for s in failures]
            
            merch_counts = Counter(failed_merchants)
            curr_counts = Counter(failed_currencies)
            
            top_merch, merch_count = merch_counts.most_common(1)[0]
            top_curr, curr_count = curr_counts.most_common(1)[0]
            
            # Lowered threshold to 40% (0.4)
            if merch_count / len(failures) > 0.4:
                return AnomalyHypothesis(
                    type="FAILURE_RATE",
                    severity="CRITICAL",
                    description=f"High failure rate ({failure_rate:.1%})",
                    root_cause_guess=f"Merchant {top_merch} is experiencing an outage.",
                    confidence=0.9
                )
            elif curr_count / len(failures) > 0.4:
                return AnomalyHypothesis(
                    type="FAILURE_RATE",
                    severity="CRITICAL",
                    description=f"High failure rate ({failure_rate:.1%})",
                    root_cause_guess=f"Payment Gateway for {top_curr} is rejecting transactions.",
                    confidence=0.85
                )
            else:
                return AnomalyHypothesis(
                    type="FAILURE_RATE",
                    severity="WARNING",
                    description=f"High failure rate ({failure_rate:.1%}) detected.",
                    root_cause_guess="Possible global system degradation or multiple failing nodes.",
                    confidence=0.6
                )
                
        # 2. Latency Spikes
        if avg_latency > 200:
            return AnomalyHypothesis(
                type="LATENCY",
                severity="WARNING",
                description=f"High average latency ({avg_latency:.0f}ms)",
                root_cause_guess="Database lock contention or network congestion.",
                confidence=0.7
            )
            
        return None  
