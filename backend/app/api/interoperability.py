from fastapi import APIRouter, Body
from typing import Dict, Any, List
from datetime import datetime, timezone
from app.protocols.validator import validate_agent_message, normalize_telemetry_metrics

router = APIRouter(prefix="/interoperability", tags=["Interoperability Lab"])

@router.post("/validate")
def validate_protocol_message(message: Dict[str, Any] = Body(...)):
    """
    Validates any incoming JSON payload against the NetCoop AI Multi-Agent Protocol.
    Returns fine-grained validation status, errors, and normalized fields.
    """
    is_valid, errors, normalized_payload = validate_agent_message(message)

    checks = {
        "schema_valid": is_valid,
        "required_fields_present": not any("Missing required field" in err for err in errors),
        "data_types_correct": not any("must be" in err for err in errors),
        "units_compatible": not any("Incompatible unit" in err for err in errors),
        "agents_recognized": not any("Invalid sender" in err or "Invalid receiver" in err for err in errors)
    }

    return {
        "is_valid": is_valid,
        "errors": errors,
        "checks": checks,
        "normalized_payload": normalized_payload,
        "validation_timestamp": datetime.now(timezone.utc).isoformat()
    }

@router.post("/send")
def send_test_message(message: Dict[str, Any] = Body(...)):
    """Simulates inter-agent message transit and response handshake."""
    is_valid, errors, normalized_payload = validate_agent_message(message)
    if not is_valid:
        return {
            "status": "rejected",
            "message": "Message rejected by NetCoop Protocol Gateway due to schema violations.",
            "errors": errors,
            "checks": {
                "schema_valid": False,
                "required_fields_present": False,
                "data_types_correct": False
            }
        }

    sender = message.get("sender")
    receiver = message.get("receiver")
    mtype = message.get("message_type")

    # Generate realistic simulated protocol response
    ack_message = {
        "message_id": f"ACK-{datetime.now(timezone.utc).strftime('%H%M%S')}",
        "sender": receiver,
        "receiver": sender,
        "message_type": "handshake_ack",
        "schema_version": "1.0",
        "timestamp": datetime.now(timezone.utc).strftime("%H:%M:%S"),
        "payload": {
            "status": "received",
            "processed_items": len(normalized_payload),
            "correlation_queue_depth": 0
        }
    }

    exchange_log = [
        {"sender": sender, "receiver": receiver, "time": datetime.now(timezone.utc).strftime("%H:%M:%S"), "status": "delivered"},
        {"sender": receiver, "receiver": sender, "time": datetime.now(timezone.utc).strftime("%H:%M:%S"), "status": "acknowledged"}
    ]

    return {
        "status": "success",
        "message": f"Message successfully validated and routed to {receiver}.",
        "errors": [],
        "checks": {
            "schema_valid": True,
            "required_fields_present": True,
            "data_types_correct": True
        },
        "ack": ack_message,
        "exchange_log": exchange_log
    }

@router.get("/schemas")
def get_protocol_schemas():
    """Returns canonical NetCoop protocol schemas and samples for the playground."""
    sample_request = {
        "message_id": "msg-7042",
        "sender": "orchestrator",
        "receiver": "performance_agent",
        "message_type": "diagnosis_request",
        "schema_version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "incident_id": "INC-1024",
            "telemetry_window": "15m",
            "device_id": "SWI-03",
            "metrics": {
                "latency_ms": 240,
                "packet_loss_pct": 3.8,
                "cpu_usage_pct": 78
            }
        }
    }

    sample_finding = {
        "message_id": "MSG-001",
        "incident_id": "INC-1024",
        "sender": "performance_agent",
        "receiver": "fault_correlation_agent",
        "message_type": "diagnostic_finding",
        "schema_version": "1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": {
            "finding": "high_network_latency",
            "severity": "high",
            "metric": "latency_ms",
            "value": 280,
            "unit": "ms",
            "device_id": "HOSTEL_CORE_SW_01",
            "evidence": ["Latency exceeds configured threshold"]
        }
    }

    return {
        "protocol_version": "NetCoop Agent v1.0",
        "schema_version": "1.0.0",
        "supported_message_types": [
            "diagnosis_request",
            "diagnostic_finding",
            "correlation_result",
            "recommendation_report",
            "telemetry_query",
            "handshake"
        ],
        "sample_templates": {
            "diagnosis_request": sample_request,
            "diagnostic_finding": sample_finding
        }
    }
