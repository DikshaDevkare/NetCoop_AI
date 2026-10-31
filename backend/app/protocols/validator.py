import re
from typing import Dict, Any, Tuple, List, Optional
from datetime import datetime

CANONICAL_FIELD_MAPPINGS = {
    "latency": "latency_ms",
    "delay": "latency_ms",
    "latency_ms": "latency_ms",
    "ping": "latency_ms",
    "rtt": "latency_ms",

    "cpu": "cpu_usage_pct",
    "cpu_usage": "cpu_usage_pct",
    "cpu_utilization": "cpu_usage_pct",
    "cpu_utilization_pct": "cpu_usage_pct",
    "cpu_pct": "cpu_usage_pct",

    "memory": "memory_usage_pct",
    "mem": "memory_usage_pct",
    "memory_usage": "memory_usage_pct",
    "memory_utilization": "memory_usage_pct",
    "memory_utilization_pct": "memory_usage_pct",

    "packetloss": "packet_loss_pct",
    "packet_loss": "packet_loss_pct",
    "packet_loss_pct": "packet_loss_pct",
    "loss": "packet_loss_pct",

    "jitter": "jitter_ms",
    "jitter_ms": "jitter_ms",

    "link_utilization": "link_utilization_pct",
    "link_utilization_pct": "link_utilization_pct",
    "bandwidth_utilization": "link_utilization_pct",
    "bandwidth_utilization_pct": "link_utilization_pct",
    "bandwidth_usage": "link_utilization_pct",

    "queue_drops": "queue_drops",
    "queuedrops": "queue_drops",
    "drops": "queue_drops",

    "interface_errors": "interface_errors",
    "errors": "interface_errors",
    "crc_errors": "interface_errors",

    "throughput": "throughput_mbps",
    "throughput_mbps": "throughput_mbps",

    "dns_response_time": "dns_resolution_time_ms",
    "dns_latency": "dns_resolution_time_ms",
    "dns_resolution_time_ms": "dns_resolution_time_ms",

    "dns_error_rate": "dns_error_rate_pct",
    "dns_error_rate_pct": "dns_error_rate_pct",

    "dhcp_latency": "dhcp_ack_latency_ms",
    "dhcp_ack_latency_ms": "dhcp_ack_latency_ms",

    "wifi_rssi": "wifi_rssi_dbm",
    "rssi": "wifi_rssi_dbm",
    "wifi_rssi_dbm": "wifi_rssi_dbm",

    "wifi_snr": "wifi_snr_db",
    "snr": "wifi_snr_db",
    "wifi_snr_db": "wifi_snr_db",

    "wifi_retrans": "wifi_retrans_pct",
    "wifi_retransmission_rate": "wifi_retrans_pct",
    "wifi_retrans_pct": "wifi_retrans_pct"
}

ALLOWED_AGENTS = {
    "orchestrator",
    "performance_agent",
    "infrastructure_agent",
    "connectivity_agent",
    "fault_correlation_agent",
    "reporting_agent",
    "external_system",
    "admin_console"
}

ALLOWED_MESSAGE_TYPES = {
    "diagnostic_finding",
    "telemetry_query",
    "correlation_result",
    "recommendation_report",
    "diagnosis_request",
    "handshake"
}

VALID_METRIC_UNITS = {
    "latency_ms": ["ms", "s", "milliseconds"],
    "packet_loss_pct": ["%", "pct", "percent"],
    "jitter_ms": ["ms", "milliseconds"],
    "cpu_usage_pct": ["%", "pct", "percent"],
    "memory_usage_pct": ["%", "pct", "percent"],
    "link_utilization_pct": ["%", "pct", "percent"],
    "queue_drops": ["pkts", "packets", "count", ""],
    "interface_errors": ["errors", "count", ""],
    "throughput_mbps": ["mbps", "gbps", "kbps"],
    "dns_resolution_time_ms": ["ms", "milliseconds"],
    "dns_error_rate_pct": ["%", "pct"],
    "dhcp_ack_latency_ms": ["ms", "milliseconds"],
    "wifi_rssi_dbm": ["dbm", "dBm"],
    "wifi_snr_db": ["db", "dB"],
    "wifi_retrans_pct": ["%", "pct"]
}

def normalize_telemetry_metrics(raw_metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize incoming raw metrics to canonical schema."""
    normalized = {}
    for raw_key, raw_val in raw_metrics.items():
        clean_key = raw_key.strip().lower()
        canonical_key = CANONICAL_FIELD_MAPPINGS.get(clean_key, clean_key)
        
        # Safe float conversion
        try:
            if raw_val is not None and not isinstance(raw_val, (dict, list)):
                if isinstance(raw_val, str):
                    # Strip units if embedded e.g. "24ms" -> 24.0
                    num_match = re.search(r"[-+]?\d*\.?\d+", raw_val)
                    if num_match:
                        raw_val = float(num_match.group(0))
                    else:
                        continue
                normalized[canonical_key] = float(raw_val)
            else:
                normalized[canonical_key] = raw_val
        except (ValueError, TypeError):
            normalized[canonical_key] = raw_val
            
    return normalized

def validate_agent_message(msg_dict: Dict[str, Any]) -> Tuple[bool, List[str], Dict[str, Any]]:
    """
    Validates agent interoperability message according to the NetCoop AI protocol.
    Returns (is_valid, errors_list, normalized_payload)
    """
    errors = []
    
    if not isinstance(msg_dict, dict):
        return False, ["Message must be a JSON object"], {}

    # Check required top-level fields
    required_fields = ["message_id", "sender", "receiver", "message_type", "schema_version", "payload"]
    for field in required_fields:
        if field not in msg_dict or msg_dict[field] is None:
            errors.append(f"Missing required field: '{field}'")

    if errors:
        return False, errors, {}

    # Validate sender and receiver
    sender = str(msg_dict.get("sender", "")).strip().lower()
    receiver = str(msg_dict.get("receiver", "")).strip().lower()

    if sender not in ALLOWED_AGENTS:
        errors.append(f"Invalid sender: '{sender}'. Must be one of {sorted(list(ALLOWED_AGENTS))}")

    if receiver not in ALLOWED_AGENTS:
        errors.append(f"Invalid receiver: '{receiver}'. Must be one of {sorted(list(ALLOWED_AGENTS))}")

    # Validate message_type
    mtype = str(msg_dict.get("message_type", "")).strip().lower()
    if mtype not in ALLOWED_MESSAGE_TYPES:
        errors.append(f"Invalid message_type: '{mtype}'. Must be one of {sorted(list(ALLOWED_MESSAGE_TYPES))}")

    # Validate schema_version
    sversion = str(msg_dict.get("schema_version", "")).strip()
    if not (sversion.startswith("1.") or sversion == "1"):
        errors.append(f"Unsupported schema_version: '{sversion}'. Supported versions: 1.0, 1.0.0")

    # Validate payload
    payload = msg_dict.get("payload")
    if not isinstance(payload, dict):
        errors.append("Field 'payload' must be a JSON dictionary object")
        return False, errors, {}

    # If payload contains metric & unit, check unit compatibility
    metric = payload.get("metric")
    unit = payload.get("unit")
    if metric:
        norm_metric = CANONICAL_FIELD_MAPPINGS.get(metric.lower(), metric.lower())
        if norm_metric in VALID_METRIC_UNITS and unit:
            allowed_units = VALID_METRIC_UNITS[norm_metric]
            if unit.lower() not in [u.lower() for u in allowed_units]:
                errors.append(f"Incompatible unit '{unit}' for metric '{metric}'. Expected one of: {allowed_units}")

    # Normalization of payload fields
    normalized_payload = {}
    for k, v in payload.items():
        if k in CANONICAL_FIELD_MAPPINGS:
            normalized_payload[CANONICAL_FIELD_MAPPINGS[k]] = v
        else:
            normalized_payload[k] = v

    return len(errors) == 0, errors, normalized_payload
