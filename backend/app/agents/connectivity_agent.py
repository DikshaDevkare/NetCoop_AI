from typing import Dict, Any, List, Optional
from app.agents.base_agent import BaseAgent

class ConnectivityAgent(BaseAgent):
    def __init__(self):
        super().__init__(agent_name="connectivity_agent")

    def analyze(self, telemetry_data: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        metrics = telemetry_data.get("normalized_metrics") or telemetry_data.get("metrics") or {}
        device_id = telemetry_data.get("device_id", "UNKNOWN_DEV")
        device_type = telemetry_data.get("device_type", "").lower()
        incident_id = (context or {}).get("incident_id")
        ml_results = (context or {}).get("ml_results", {})

        evidence = []
        severity = "low"
        confidence = 0.50

        # Check DNS/DHCP
        dns_time = float(metrics.get("dns_resolution_time_ms", 0.0) or 0.0)
        dns_err_rate = float(metrics.get("dns_error_rate_pct", 0.0) or 0.0)
        dhcp_lat = float(metrics.get("dhcp_ack_latency_ms", 0.0) or 0.0)

        if dns_time > 1000.0 or dns_err_rate > 30.0:
            evidence.append(f"Severe DNS latency/failures: {dns_time:.1f}ms latency, {dns_err_rate:.1f}% error rate")
            severity = "high"
            confidence += 0.25

        if dhcp_lat > 2000.0:
            evidence.append(f"DHCP ACK timeout/delay: {dhcp_lat:.1f}ms")
            severity = "high"
            confidence += 0.20

        # Wi-Fi Checks: Strictly evaluate ONLY if Wi-Fi metrics exist and device is an Access Point or Wi-Fi client
        # Rule: Do not interpret missing Wi-Fi metrics on a wired device as a weak signal.
        has_wifi_metrics = "wifi_rssi_dbm" in metrics and metrics.get("wifi_rssi_dbm") is not None
        is_wireless = "ap" in device_type or "access point" in device_type or "wifi" in device_type or "wireless" in device_type

        if has_wifi_metrics and (is_wireless or "AP_" in device_id):
            rssi = float(metrics.get("wifi_rssi_dbm", 0.0) or 0.0)
            snr = float(metrics.get("wifi_snr_db", 0.0) or 0.0)
            retrans = float(metrics.get("wifi_retrans_pct", 0.0) or 0.0)

            if rssi < -78.0:
                evidence.append(f"Sub-optimal Wi-Fi RSSI signal: {rssi:.1f} dBm")
                severity = "medium" if severity == "low" else severity
                confidence += 0.15

            if snr < 12.0:
                evidence.append(f"Poor Wi-Fi SNR: {snr:.1f} dB (excess RF interference)")
                confidence += 0.10

            if retrans > 25.0:
                evidence.append(f"High 802.11 frame retransmissions: {retrans:.1f}%")
                confidence += 0.15

        # ML Fault model verification
        xgb_res = ml_results.get("xgboost", {})
        predicted_fault = xgb_res.get("predicted_fault")
        if predicted_fault in ("dns_dhcp_failure", "weak_wifi"):
            evidence.append(f"ML Classifier corroborates connectivity issue: '{predicted_fault}'")
            confidence += 0.15

        confidence = min(0.96, max(0.30, confidence))

        primary_finding = "connectivity_normal"
        if dns_time > 1000.0 or dns_err_rate > 30.0 or dhcp_lat > 2000.0:
            primary_finding = "dns_dhcp_failure"
        elif has_wifi_metrics and (is_wireless or "AP_" in device_id) and any("Wi-Fi" in e for e in evidence):
            primary_finding = "weak_wifi_signal"
        elif evidence:
            primary_finding = "connectivity_anomaly"

        msg = self.create_message(
            receiver="fault_correlation_agent",
            message_type="diagnostic_finding",
            incident_id=incident_id,
            payload={
                "finding": primary_finding,
                "severity": severity,
                "metric": "dns_resolution_time_ms" if primary_finding == "dns_dhcp_failure" else "wifi_rssi_dbm",
                "value": dns_time if primary_finding == "dns_dhcp_failure" else metrics.get("wifi_rssi_dbm", 0.0),
                "unit": "ms" if primary_finding == "dns_dhcp_failure" else "dBm",
                "device_id": device_id,
                "evidence": evidence,
                "metadata": {
                    "dns_error_rate_pct": dns_err_rate,
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
