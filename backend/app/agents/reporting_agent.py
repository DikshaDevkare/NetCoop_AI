from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent

ACTION_PLAYBOOK = {
    "Interface congestion": [
        {"action_id": "ACT-01", "title": "Apply rate limiting on switch uplink", "status": "recommended", "priority": "high"},
        {"action_id": "ACT-02", "title": "Review QoS policy and prioritize mission-critical queues", "status": "recommended", "priority": "high"},
        {"action_id": "ACT-03", "title": "Monitor queue utilization and buffer allocation", "status": "in_review", "priority": "medium"},
        {"action_id": "ACT-04", "title": "Validate interface latency after 15 minutes", "status": "pending", "priority": "medium"}
    ],
    "Hardware / ASIC failure": [
        {"action_id": "ACT-05", "title": "Initiate automated failover to redundant standby node", "status": "recommended", "priority": "critical"},
        {"action_id": "ACT-06", "title": "Dispatch campus technician for hardware chassis inspection", "status": "recommended", "priority": "high"},
        {"action_id": "ACT-07", "title": "Collect core dump and system event logs before reboot", "status": "pending", "priority": "medium"}
    ],
    "Physical layer / Interface CRC fault": [
        {"action_id": "ACT-08", "title": "Perform optical transceiver DOM diagnostic check", "status": "recommended", "priority": "high"},
        {"action_id": "ACT-09", "title": "Clean or replace physical patch cable on designated port", "status": "recommended", "priority": "high"},
        {"action_id": "ACT-10", "title": "Reset interface counters and observe error recurrence", "status": "pending", "priority": "medium"}
    ],
    "Core DNS/DHCP resolver failure": [
        {"action_id": "ACT-11", "title": "Verify bind9 / dnsmasq service daemon status on core resolver", "status": "recommended", "priority": "critical"},
        {"action_id": "ACT-12", "title": "Flush DNS resolver cache and test upstream forwarders", "status": "recommended", "priority": "high"},
        {"action_id": "ACT-13", "title": "Inspect DHCP pool allocation exhausted state", "status": "in_review", "priority": "high"}
    ],
    "RF degradation / Weak Wi-Fi signal": [
        {"action_id": "ACT-14", "title": "Check Access Point transmit power (Tx power) settings", "status": "recommended", "priority": "medium"},
        {"action_id": "ACT-15", "title": "Analyze 2.4GHz / 5GHz RF co-channel interference levels", "status": "recommended", "priority": "medium"},
        {"action_id": "ACT-16", "title": "Conduct physical survey of access point coverage zone", "status": "pending", "priority": "low"}
    ],
    "Upstream transit latency spike": [
        {"action_id": "ACT-17", "title": "Execute MTR / traceroute to upstream ISP edge router", "status": "recommended", "priority": "medium"},
        {"action_id": "ACT-18", "title": "Verify BGP route stability and peering prefix health", "status": "in_review", "priority": "medium"}
    ],
    "Control plane CPU starvation": [
        {"action_id": "ACT-19", "title": "Inspect top processes utilizing switch control plane CPU", "status": "recommended", "priority": "high"},
        {"action_id": "ACT-20", "title": "Enable Control Plane Policing (CoPP) against broadcast floods", "status": "recommended", "priority": "high"}
    ]
}

DEFAULT_ACTIONS = [
    {"action_id": "ACT-99", "title": "Verify telemetry metrics against baseline", "status": "recommended", "priority": "low"},
    {"action_id": "ACT-100", "title": "Continue standard telemetry monitoring", "status": "recommended", "priority": "low"}
]

class ReportingAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="reporting_agent")

    def generate_report(
        self,
        correlation_result: Dict[str, Any],
        incident_id: str,
        telemetry_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Synthesizes correlated findings into an explainable, structured diagnosis report.
        """
        corr = correlation_result.get("correlation", {})
        root_cause = corr.get("probable_root_cause", "Normal network operations")
        confidence = float(corr.get("confidence", 0.85))
        confidence_pct = int(confidence * 100)
        supporting_evidence = corr.get("supporting_evidence", [])
        alternative_causes = corr.get("alternative_causes", [])
        affected_device = corr.get("affected_device", telemetry_data.get("device_id", "CAMPUS_SW"))

        # Determine recommended actions matching root cause category
        recommended_actions = []
        for key, actions in ACTION_PLAYBOOK.items():
            if key.lower() in root_cause.lower():
                recommended_actions = actions
                break
        if not recommended_actions:
            recommended_actions = DEFAULT_ACTIONS

        # Clear honest limitations statement
        limitations = [
            "Telemetry records may be simulated or synthetic based on simulation mode flag.",
            "Confidence derived from multi-agent probabilistic and deterministic scoring.",
            "Diagnosis recommends corrective actions; administrator validation required before executing network configuration changes.",
            "Historical telemetry horizon evaluated based on available sliding window."
        ]

        # Structure evidence correlation graph nodes for visualization
        evidence_graph = {
            "center": {"id": "root_cause", "label": "Root Cause", "name": root_cause, "confidence": confidence},
            "nodes": [
                {
                    "id": f"ev-{i}",
                    "label": ev[:45] + ("..." if len(ev) > 45 else ""),
                    "full_text": ev,
                    "weight": round(max(0.60, min(0.95, confidence - 0.05 * i)), 2)
                }
                for i, ev in enumerate(supporting_evidence[:5])
            ]
        }

        report_dict = {
            "incident_id": incident_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "root_cause": root_cause,
            "confidence": confidence,
            "confidence_pct": confidence_pct,
            "affected_device": affected_device,
            "supporting_evidence": supporting_evidence,
            "alternative_causes": alternative_causes,
            "recommended_actions": recommended_actions,
            "evidence_graph": evidence_graph,
            "limitations": limitations,
            "agent_signoff": "NetCoop AI Multi-Agent Diagnostic Engine v1.0"
        }

        msg = self.create_message(
            receiver="orchestrator",
            message_type="recommendation_report",
            incident_id=incident_id,
            payload=report_dict
        )

        return {
            "agent": self.agent_name,
            "status": "completed",
            "report": report_dict,
            "message": msg
        }
