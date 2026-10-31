from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent

class PerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="performance_agent")

    def analyze(self, telemetry_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        metrics = telemetry_data.get("normalized_metrics") or telemetry_data.get("metrics") or {}
        device_id = telemetry_data.get("device_id", "UNKNOWN_DEV")
        incident_id = (context or {}).get("incident_id")
        ml_results = (context or {}).get("ml_results", {})
        temporal_analysis = (context or {}).get("temporal_analysis", {})

        findings = []
        evidence = []
        severity = "low"
        confidence = 0.50

        latency = float(metrics.get("latency_ms", 0.0) or 0.0)
        packet_loss = float(metrics.get("packet_loss_pct", 0.0) or 0.0)
        jitter = float(metrics.get("jitter_ms", 0.0) or 0.0)
        link_util = float(metrics.get("link_utilization_pct", 0.0) or 0.0)
        queue_drops = int(metrics.get("queue_drops", 0) or 0)
        throughput = float(metrics.get("throughput_mbps", 0.0) or 0.0)

        # 1. Deterministic Rule Checks
        if latency > 150.0:
            evidence.append(f"Elevated latency observed: {latency:.1f}ms (threshold 100ms)")
            severity = "high" if latency > 300.0 else "medium"
            confidence += 0.15

        if packet_loss > 1.0:
            evidence.append(f"Abnormal packet loss: {packet_loss:.2f}% (normal < 0.2%)")
            severity = "critical" if packet_loss > 10.0 else "high"
            confidence += 0.15

        if link_util > 85.0:
            evidence.append(f"High link saturation: {link_util:.1f}% link utilization")
            severity = "high"
            confidence += 0.15

        if queue_drops > 100:
            evidence.append(f"Egress queue drops detected: {queue_drops} dropped packets")
            confidence += 0.10

        # 2. ML Anomaly Integration (Model 1)
        iso_res = ml_results.get("isolation_forest", {})
        if iso_res.get("is_anomaly"):
            evidence.append(f"Isolation Forest flagged anomaly with score {iso_res.get('anomaly_score', 0):.2f}")
            confidence += 0.10

        # 3. ML Fault Classification Integration (Model 2)
        xgb_res = ml_results.get("xgboost", {})
        predicted_fault = xgb_res.get("predicted_fault")
        if predicted_fault in ("congestion", "latency_spike"):
            evidence.append(f"XGBoost classified fault as '{predicted_fault}' ({xgb_res.get('confidence', 0)*100:.1f}% prob)")
            confidence += 0.15

        # 4. Temporal Trend Integration
        temp_metrics = temporal_analysis.get("metrics", {})
        lat_trend = temp_metrics.get("latency_ms", {})
        if lat_trend.get("direction") == "increasing":
            evidence.append(f"Temporal analysis confirms escalating latency trend (+{lat_trend.get('delta', 0):.1f}ms)")
            confidence += 0.08

        # Cap confidence
        confidence = min(0.96, max(0.30, confidence))

        primary_finding = "normal_performance"
        if link_util > 85.0 and queue_drops > 200:
            primary_finding = "network_congestion"
        elif latency > 180.0 and packet_loss < 2.0:
            primary_finding = "latency_spike"
        elif packet_loss > 5.0:
            primary_finding = "packet_loss_degradation"
        elif evidence:
            primary_finding = "performance_anomaly"

        # Create structured inter-agent message to fault correlation agent
        msg = self.create_message(
            receiver="fault_correlation_agent",
            message_type="diagnostic_finding",
            incident_id=incident_id,
            payload={
                "finding": primary_finding,
                "severity": severity,
                "metric": "latency_ms",
                "value": latency,
                "unit": "ms",
                "device_id": device_id,
                "evidence": evidence,
                "metadata": {
                    "link_utilization_pct": link_util,
                    "packet_loss_pct": packet_loss,
                    "queue_drops": queue_drops,
                    "confidence": round(confidence, 4)
                }
            }
        )

        return {
            "agent": self.agent_name,
            "status": "completed",
            "primary_finding": primary_finding,
            "severity": severity,
            "confidence": round(confidence, 4),
            "evidence": evidence,
            "message": msg
        }
