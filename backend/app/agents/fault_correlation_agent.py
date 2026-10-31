from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent

class FaultCorrelationAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="fault_correlation_agent")

    def correlate(
        self,
        agent_findings: List[Dict[str, Any]],
        ml_results: Dict[str, Any],
        temporal_analysis: Dict[str, Any],
        telemetry_data: Dict[str, Any],
        incident_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Correlates multiple diagnostic streams using multi-factor evidence weighting.
        Detects conflicts, reduces confidence when contradictory, and surfaces alternative hypotheses.
        """
        device_id = telemetry_data.get("device_id", "CAMPUS_DEV")
        hypotheses: Dict[str, Dict[str, Any]] = {}

        def add_hypothesis(cause: str, score: float, evidence_str: str, source: str):
            if cause not in hypotheses:
                hypotheses[cause] = {
                    "cause": cause,
                    "score": 0.0,
                    "evidence": [],
                    "sources": set()
                }
            hypotheses[cause]["score"] += score
            hypotheses[cause]["evidence"].append(evidence_str)
            hypotheses[cause]["sources"].add(source)

        # 1. Correlate findings from domain agents
        for f in agent_findings:
            agent = f.get("agent")
            finding = f.get("primary_finding")
            conf = float(f.get("confidence", 0.5))
            f_evidence = f.get("evidence", [])

            if finding == "network_congestion":
                add_hypothesis("Interface congestion on " + device_id, conf * 0.45, f"Performance Agent detected saturated link & queue backlog", agent)
            elif finding == "latency_spike":
                add_hypothesis("Upstream transit latency spike", conf * 0.40, f"Performance Agent detected sudden round-trip time expansion", agent)
            elif finding == "hardware_failure":
                add_hypothesis("Hardware / ASIC failure on " + device_id, conf * 0.50, f"Infrastructure Agent reported maxed CPU/memory with high packet drop", agent)
            elif finding == "interface_hardware_fault":
                add_hypothesis("Physical layer / Interface CRC fault on " + device_id, conf * 0.45, f"Infrastructure Agent found excessive interface CRC error counters", agent)
            elif finding == "cpu_overload":
                add_hypothesis("Control plane CPU starvation on " + device_id, conf * 0.40, f"Infrastructure Agent identified sustained high processor load", agent)
            elif finding == "dns_dhcp_failure":
                add_hypothesis("Core DNS/DHCP resolver failure", conf * 0.50, f"Connectivity Agent verified DNS query timeouts and DHCP delay", agent)
            elif finding == "weak_wifi_signal":
                add_hypothesis("RF degradation / Weak Wi-Fi signal at " + device_id, conf * 0.45, f"Connectivity Agent verified low RSSI and high 802.11 retransmissions", agent)

            for ev in f_evidence:
                if finding in hypotheses:
                    hypotheses[finding]["evidence"].append(ev)

        # 2. Correlate ML Models
        xgb_res = ml_results.get("xgboost", {})
        predicted_fault = xgb_res.get("predicted_fault")
        xgb_conf = float(xgb_res.get("confidence", 0.0))

        if predicted_fault and predicted_fault != "normal":
            mapped_cause = {
                "congestion": f"Interface congestion on {device_id}",
                "latency_spike": "Upstream transit latency spike",
                "hardware_failure": f"Hardware / ASIC failure on {device_id}",
                "interface_fault": f"Physical layer / Interface CRC fault on {device_id}",
                "dns_dhcp_failure": "Core DNS/DHCP resolver failure",
                "weak_wifi": f"RF degradation / Weak Wi-Fi signal at {device_id}"
            }.get(predicted_fault, predicted_fault)
            
            add_hypothesis(mapped_cause, xgb_conf * 0.35, f"Trained XGBoost model classified {predicted_fault} with {xgb_conf*100:.1f}% confidence", "ml_xgboost")

        rf_res = ml_results.get("random_forest", {})
        rf_cond = rf_res.get("predicted_condition")
        if rf_cond and rf_cond != "normal":
            mapped_rf = {
                "queue_congestion": f"Interface congestion on {device_id}",
                "hardware_failure": f"Hardware / ASIC failure on {device_id}",
                "interface_failure": f"Physical layer / Interface CRC fault on {device_id}",
                "cpu_overload": f"Control plane CPU starvation on {device_id}"
            }.get(rf_cond)
            if mapped_rf:
                add_hypothesis(mapped_rf, float(rf_res.get("confidence", 0.5)) * 0.25, f"Trained Random Forest classified infrastructure state '{rf_cond}'", "ml_rf")

        # 3. Detect Evidence Conflicts
        has_perf_congestion = any(f.get("primary_finding") == "network_congestion" for f in agent_findings)
        has_infra_healthy = any(f.get("primary_finding") == "healthy_infrastructure" for f in agent_findings)
        has_dns_issue = any(f.get("primary_finding") == "dns_dhcp_failure" for f in agent_findings)

        conflict_detected = False
        conflict_notes = []
        if has_dns_issue and has_perf_congestion:
            conflict_detected = True
            conflict_notes.append("Conflicting observations: Both transport congestion and application-layer DNS delays observed simultaneously.")

        # 4. Rank Hypotheses
        sorted_hypotheses = sorted(hypotheses.values(), key=lambda h: h["score"], reverse=True)

        if not sorted_hypotheses:
            probable_cause = "Normal network operations - No anomalous root cause identified"
            final_confidence = 0.90
            alternatives = []
            all_evidence = ["All metrics within normal operational thresholds"]
        else:
            top_hyp = sorted_hypotheses[0]
            probable_cause = top_hyp["cause"]
            
            # Compute confidence normalized to [0.55, 0.94]
            raw_conf = min(0.95, max(0.50, top_hyp["score"] / 1.1))
            if conflict_detected:
                raw_conf *= 0.85 # Penalty for conflicting evidence
            final_confidence = round(raw_conf, 2)

            all_evidence = list(dict.fromkeys(top_hyp["evidence"])) # Deduplicate preserving order
            alternatives = [
                {
                    "cause": h["cause"],
                    "relative_confidence": round(min(0.85, h["score"] / max(0.1, top_hyp["score"]) * final_confidence), 2),
                    "evidence_summary": h["evidence"][:2]
                }
                for h in sorted_hypotheses[1:4]
            ]

        correlation_payload = {
            "probable_root_cause": probable_cause,
            "confidence": final_confidence,
            "confidence_pct": int(final_confidence * 100),
            "conflict_detected": conflict_detected,
            "conflict_notes": conflict_notes,
            "supporting_evidence": all_evidence,
            "alternative_causes": alternatives,
            "affected_device": device_id
        }

        msg = self.create_message(
            receiver="reporting_agent",
            message_type="correlation_result",
            incident_id=incident_id,
            payload=correlation_payload
        )

        return {
            "agent": self.agent_name,
            "status": "completed",
            "correlation": correlation_payload,
            "message": msg
        }
