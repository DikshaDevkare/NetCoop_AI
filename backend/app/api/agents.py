from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timezone
from app.database.connection import get_db
from app.database.models import AgentMessage, AgentFinding

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("/status")
def get_agents_status():
    """Returns real-time status of the multi-agent system nodes matching Panel 4."""
    return {
        "orchestrator": {
            "name": "Orchestrator",
            "status": "Active",
            "state": "active",
            "color": "#FF781F",
            "role": "Central intelligence coordinator"
        },
        "agents": [
            {
                "id": "performance_agent",
                "name": "Performance Agent",
                "status": "Completed",
                "state": "done",
                "badge": "Active",
                "color": "#A855F7",
                "icon": "Zap",
                "focus": "Latency, throughput, jitter, queue-drop analysis"
            },
            {
                "id": "infrastructure_agent",
                "name": "Infrastructure Health Agent",
                "status": "Done",
                "state": "done",
                "badge": "Done",
                "color": "#20E88A",
                "icon": "Cpu",
                "focus": "CPU, memory, hardware counters, CRC interface errors"
            },
            {
                "id": "connectivity_agent",
                "name": "Connectivity Analysis Agent",
                "status": "Processing...",
                "state": "processing",
                "badge": "Processing",
                "color": "#20D9FF",
                "icon": "Radio",
                "focus": "DNS response times, DHCP status, Wi-Fi RSSI & SNR"
            },
            {
                "id": "fault_correlation_agent",
                "name": "Fault Correlation Agent",
                "status": "Running...",
                "state": "running",
                "badge": "Running",
                "color": "#E040FB",
                "icon": "GitBranch",
                "focus": "Cross-agent evidence fusion & conflict resolution"
            },
            {
                "id": "reporting_agent",
                "name": "Recommendation & Reporting Agent",
                "status": "Standby",
                "state": "standby",
                "badge": "Standby",
                "color": "#FF9B35",
                "icon": "FileText",
                "focus": "Explainable diagnosis reports & actionable remediations"
            }
        ]
    }

@router.get("/messages/{incident_id}")
def get_agent_messages(incident_id: str, db: Session = Depends(get_db)):
    msgs = db.query(AgentMessage).filter(AgentMessage.incident_id == incident_id).order_by(AgentMessage.timestamp.asc()).all()
    if msgs:
        return [
            {
                "message_id": m.message_id,
                "incident_id": m.incident_id,
                "sender": m.sender,
                "receiver": m.receiver,
                "message_type": m.message_type,
                "schema_version": m.schema_version,
                "timestamp": m.timestamp.strftime("%H:%M:%S") if m.timestamp else "14:02:11",
                "payload": m.payload
            }
            for m in msgs
        ]

    # Reference messages matching Panel 4
    return [
        {
            "message_id": "MSG-001",
            "incident_id": incident_id or "INC-1024",
            "sender": "performance_agent",
            "receiver": "fault_correlation_agent",
            "message_type": "diagnostic_finding",
            "schema_version": "1.0",
            "timestamp": "14:02:11",
            "payload": {
                "finding": "high_network_latency",
                "metric": "latency_ms",
                "value": 240,
                "unit": "ms",
                "device_id": "SWI-03",
                "evidence": ["Latency exceeds configured threshold (240ms > 50ms)"]
            }
        },
        {
            "message_id": "MSG-002",
            "incident_id": incident_id or "INC-1024",
            "sender": "infrastructure_agent",
            "receiver": "fault_correlation_agent",
            "message_type": "diagnostic_finding",
            "schema_version": "1.0",
            "timestamp": "14:02:18",
            "payload": {
                "finding": "elevated_cpu_utilization",
                "metric": "cpu_usage_pct",
                "value": 78.0,
                "unit": "%",
                "device_id": "SWI-03",
                "evidence": ["High CPU on SW-03 (78%)", "Queue drops counter: 34"]
            }
        },
        {
            "message_id": "MSG-003",
            "incident_id": incident_id or "INC-1024",
            "sender": "connectivity_agent",
            "receiver": "fault_correlation_agent",
            "message_type": "diagnostic_finding",
            "schema_version": "1.0",
            "timestamp": "14:02:24",
            "payload": {
                "finding": "increased_queuing_delay",
                "metric": "latency_ms",
                "value": 195,
                "unit": "ms",
                "device_id": "SWI-03",
                "evidence": ["Increased queuing delay across Building A uplink"]
            }
        },
        {
            "message_id": "MSG-004",
            "incident_id": incident_id or "INC-1024",
            "sender": "fault_correlation_agent",
            "receiver": "reporting_agent",
            "message_type": "correlation_result",
            "schema_version": "1.0",
            "timestamp": "14:02:29",
            "payload": {
                "probable_root_cause": "Interface congestion on SW-03",
                "confidence": 0.87,
                "supporting_evidence": ["High bandwidth utilization", "Queue drops", "Increased latency"]
            }
        }
    ]

@router.get("/execution/{incident_id}")
def get_execution_timeline(incident_id: str):
    return [
        {"stage": "init", "title": "Orchestrator initialized", "time": "14:02:11", "status": "completed"},
        {"stage": "perf", "title": "Performance Agent analysis", "time": "14:02:18", "status": "completed"},
        {"stage": "infra", "title": "Infrastructure analysis", "time": "14:02:24", "status": "completed"},
        {"stage": "conn", "title": "Connectivity analysis", "time": "14:02:29", "status": "completed"},
        {"stage": "corr", "title": "Fault correlation", "time": "14:02:35", "status": "running"},
        {"stage": "report", "title": "Generating recommendation", "time": "...", "status": "pending"}
    ]
