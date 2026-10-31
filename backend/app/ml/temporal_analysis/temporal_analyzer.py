import numpy as np
import pandas as pd
from typing import Dict, Any, List

class TemporalTelemetryAnalyzer:
    """
    Chronological telemetry analyzer examining rolling trends, rates of change,
    volatility, persistence, and recovery behavior strictly within incident/device bounds.
    """

    def analyze_sequence(self, telemetry_records: List[Dict[str, Any]], window_size: int = 5) -> Dict[str, Any]:
        if not telemetry_records:
            return {"status": "insufficient_data", "metrics": {}}

        # Extract rows
        rows = []
        for r in telemetry_records:
            metrics = r.get("normalized_metrics") or r.get("metrics") or r
            rows.append({
                "latency_ms": float(metrics.get("latency_ms", 0.0) or 0.0),
                "packet_loss_pct": float(metrics.get("packet_loss_pct", 0.0) or 0.0),
                "jitter_ms": float(metrics.get("jitter_ms", 0.0) or 0.0),
                "cpu_usage_pct": float(metrics.get("cpu_usage_pct", 0.0) or 0.0),
                "memory_usage_pct": float(metrics.get("memory_usage_pct", 0.0) or 0.0),
                "link_utilization_pct": float(metrics.get("link_utilization_pct", 0.0) or 0.0),
                "queue_drops": float(metrics.get("queue_drops", 0.0) or 0.0),
                "interface_errors": float(metrics.get("interface_errors", 0.0) or 0.0)
            })

        df = pd.DataFrame(rows)
        n = len(df)

        analysis = {
            "sample_count": n,
            "metrics": {},
            "recovery_detected": False,
            "overall_trajectory": "stable"
        }

        # Analyze key signals
        for col in ["latency_ms", "packet_loss_pct", "cpu_usage_pct", "link_utilization_pct", "queue_drops"]:
            series = df[col]
            current_val = float(series.iloc[-1])
            mean_val = float(series.mean())
            std_val = float(series.std(ddof=0)) if n > 1 else 0.0
            
            # Rate of change: (last - first)
            first_val = float(series.iloc[0])
            delta = current_val - first_val
            pct_change = ((current_val - first_val) / max(0.1, abs(first_val))) * 100.0 if n > 1 else 0.0

            # Rolling stats (strictly backward looking)
            rolling_avg = float(series.tail(min(window_size, n)).mean())

            # Trend direction
            if delta > (std_val * 0.75 + 1.0):
                direction = "increasing"
            elif delta < -(std_val * 0.75 + 1.0):
                direction = "decreasing"
            else:
                direction = "stable"

            # Persistence: count of consecutive abnormal values above mean + 1 std
            threshold = mean_val + max(std_val, 2.0)
            persistent_count = int((series.tail(min(window_size, n)) > threshold).sum())

            analysis["metrics"][col] = {
                "current": round(current_val, 2),
                "mean": round(mean_val, 2),
                "std": round(std_val, 2),
                "rolling_avg": round(rolling_avg, 2),
                "delta": round(delta, 2),
                "pct_change": round(pct_change, 2),
                "direction": direction,
                "persistent_high_steps": persistent_count
            }

        # Detect recovery behavior: if earlier spikes declined back near baseline
        latency_info = analysis["metrics"].get("latency_ms", {})
        cpu_info = analysis["metrics"].get("cpu_usage_pct", {})
        if latency_info.get("direction") == "decreasing" and cpu_info.get("direction") in ("decreasing", "stable"):
            if latency_info.get("current", 0.0) < latency_info.get("mean", 0.0):
                analysis["recovery_detected"] = True
                analysis["overall_trajectory"] = "recovering"

        if not analysis["recovery_detected"]:
            if any(info.get("direction") == "increasing" and info.get("persistent_high_steps", 0) >= 3 for info in analysis["metrics"].values()):
                analysis["overall_trajectory"] = "degrading"
            elif any(info.get("direction") == "increasing" for info in analysis["metrics"].values()):
                analysis["overall_trajectory"] = "fluctuating"

        return analysis
