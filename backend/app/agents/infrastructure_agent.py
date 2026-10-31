from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent

class InfrastructureAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="infrastructure_agent")

    def analyze(self, telemetry_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        metrics = telemetry_data.get("normalized_metrics") or telemetry_data.get("metrics") or {}
        device_id = telemetry_data.get("device_id", "UNKNOWN_DEV")
        incident_id = (context or {}).get("incident_id")
        ml_results = (context or {}).get("ml_results", {})

        findings = []
        evidence = []
        severity = "low"
        confidence = 0.50

        cpu = float(metrics.get("cpu_usage_pct", 0.0) or 0.0)
        memory = float(metrics.get("memory_usage_pct", 0.0) or 0.0)
        interface_errors = int(metrics.get("interface_errors", 0) or 0)
        queue_drops = int(metrics.get("queue_drops", 0) or 0)

        # 1. Deterministic Rule Checks
        if cpu > 90.0:
            evidence.append(f"Critical CPU exhaustion: {cpu:.1f}%")
            severity = "critical" if cpu > 98.0 else "high"
            confidence += 0.20
        elif cpu > 75.0:
            evidence.append(f"Elevated CPU load: {cpu:.1f}%")
            severity = "medium"
            confidence += 0.10

        if memory > 88.0:
            evidence.append(f"High memory saturation: {memory:.1f}%")
            confidence += 0.15

        if interface_errors > 100:
            evidence.append(f"Physical interface/CRC errors detected: {interface_errors} errors")
            severity = "critical" if interface_errors > 500 else "high"
            confidence += 0.20

        if queue_drops > 1000:
            evidence.append(f"Hardware buffer overflow: {queue_drops} queue drops")
            confidence += 0.15

        # 2. ML Infrastructure Classifier (Model 3)
        rf_res = ml_results.get("random_forest", {})
        rf_condition = rf_res.get("predicted_condition")
        if rf_condition and rf_condition != "normal":
            evidence.append(f"Random Forest predicted infrastructure fault: '{rf_condition}' (conf {rf_res.get('confidence', 0)*100:.1f}%)")
            confidence += 0.15

        confidence = min(0.96, max(0.30, confidence))

        primary_finding = "healthy_infrastructure"
        if cpu > 95.0 and memory > 90.0:
            primary_finding = "hardware_failure"
        elif interface_errors > 150:
            primary_finding = "interface_hardware_fault"
        elif cpu > 85.0:
            primary_finding = "cpu_overload"
        elif evidence:
            primary_finding = "infrastructure_strain"

        msg = self.create_message(
            receiver="fault_correlation_agent",
            message_type="diagnostic_finding",
            incident_id=incident_id,
            payload={
                "finding": primary_finding,
                "severity": severity,
                "metric": "cpu_usage_pct",
                "value": cpu,
                "unit": "%",
                "device_id": device_id,
                "evidence": evidence,
                "metadata": {
                    "memory_usage_pct": memory,
                    "interface_errors": interface_errors,
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
