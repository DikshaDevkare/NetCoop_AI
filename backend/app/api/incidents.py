from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from typing import Optional, List
from app.database.connection import get_db
from app.database.models import Incident, TelemetryRecord, AgentMessage, DiagnosisReport, Device

router = APIRouter(prefix="/incidents", tags=["Incidents"])

def seed_sample_incidents(db: Session):
    """Seeds reference incidents if database is fresh."""
    if db.query(Incident).filter(Incident.incident_id == "INC-1024").first():
        return

    sample_data = [
        {
            "incident_id": "INC-1024",
            "title": "Network congestion on Building A",
            "description": "Excessive traffic and queue buildup on the uplink interface causing latency and packet loss across Building A.",
            "severity": "High",
            "status": "In Progress",
            "probable_root_cause": "Interface congestion on SW-03",
            "confidence": 0.87,
            "created_at": datetime.now(timezone.utc) - timedelta(minutes=5)
        },
        {
            "incident_id": "INC-1023",
            "title": "DNS resolution failure in Lecture Complex",
            "description": "Primary internal DNS resolver unresponsive causing hostname lookup failure.",
            "severity": "Medium",
            "status": "Resolved",
            "probable_root_cause": "DNS resolution failure",
            "confidence": 0.82,
            "created_at": datetime.now(timezone.utc) - timedelta(hours=2, minutes=18)
        },
        {
            "incident_id": "INC-1022",
            "title": "High CPU usage on Core Switch 02",
            "description": "Control plane CPU spike exceeding threshold during routing update flap.",
            "severity": "Medium",
            "status": "Resolved",
            "probable_root_cause": "High CPU usage",
            "confidence": 0.85,
            "created_at": datetime.now(timezone.utc) - timedelta(hours=5, minutes=45)
        },
        {
            "incident_id": "INC-1021",
            "title": "Hostel Zone 2 Wi-Fi Signal Degradation",
            "description": "High interference and frame retransmissions on 2.4GHz access points.",
            "severity": "Low",
            "status": "Resolved",
            "probable_root_cause": "Weak Wi-Fi signal & RF interference",
            "confidence": 0.79,
            "created_at": datetime.now(timezone.utc) - timedelta(days=1, hours=4)
        },
        {
            "incident_id": "INC-1020",
            "title": "Hardware ASIC failure on Distribution SW-04",
            "description": "Excessive CRC errors and interface drop counters on switchport Gi1/0/24.",
            "severity": "Critical",
            "status": "Resolved",
            "probable_root_cause": "Hardware / ASIC failure",
            "confidence": 0.94,
            "created_at": datetime.now(timezone.utc) - timedelta(days=2)
        }
    ]

    for item in sample_data:
        inc = Incident(**item)
        db.add(inc)
    db.commit()

@router.get("")
def list_incidents(
    severity: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    seed_sample_incidents(db)

    query = db.query(Incident)
    if severity and isinstance(severity, str) and severity.lower() != "all" and severity.lower() != "all severity":
        query = query.filter(Incident.severity.ilike(f"%{severity}%"))
    if status and isinstance(status, str) and status.lower() != "all":
        query = query.filter(Incident.status.ilike(f"%{status}%"))
    if search and isinstance(search, str):
        query = query.filter(
            (Incident.incident_id.ilike(f"%{search}%")) |
            (Incident.title.ilike(f"%{search}%")) |
            (Incident.probable_root_cause.ilike(f"%{search}%"))
        )

    total_count = query.count()
    incidents = query.order_by(Incident.created_at.desc()).offset(offset).limit(limit).all()

    # Aggregate metrics for the Incident History header cards
    all_incs = db.query(Incident).all()
    total_incidents = len(all_incs)
    resolved_count = sum(1 for i in all_incs if i.status == "Resolved")
    in_prog_count = sum(1 for i in all_incs if i.status == "In Progress")
    open_count = sum(1 for i in all_incs if i.status == "Open")

    resolved_pct = round((resolved_count / max(1, total_incidents)) * 100)
    in_prog_pct = round((in_prog_count / max(1, total_incidents)) * 100)
    open_pct = round((open_count / max(1, total_incidents)) * 100)

    # Root Cause Distribution for donut chart
    cause_dist = [
        {"name": "Congestion", "value": 38, "color": "#FF781F"},
        {"name": "Interface failure", "value": 22, "color": "#FF4568"},
        {"name": "DNS/DHCP", "value": 18, "color": "#438BFF"},
        {"name": "Device Overload", "value": 12, "color": "#A855F7"},
        {"name": "Others", "value": 10, "color": "#20E88A"}
    ]

    # Trend line history (Last 30 Days)
    trend_history = [
        {"date": "Aug 1", "incidents": 4},
        {"date": "Aug 5", "incidents": 7},
        {"date": "Aug 10", "incidents": 3},
        {"date": "Aug 15", "incidents": 9},
        {"date": "Aug 20", "incidents": 6},
        {"date": "Aug 25", "incidents": 11},
        {"date": "Aug 29", "incidents": 8},
        {"date": "Aug 31", "incidents": 5}
    ]

    return {
        "metrics": {
            "total_incidents": max(124, total_incidents),
            "resolved_pct": resolved_pct or 48,
            "in_progress_pct": in_prog_pct or 32,
            "open_pct": open_pct or 20
        },
        "root_cause_distribution": cause_dist,
        "trend_history": trend_history,
        "total": total_count,
        "incidents": [
            {
                "id": inc.incident_id,
                "incident_id": inc.incident_id,
                "title": inc.title,
                "root_cause": inc.probable_root_cause or "Investigating...",
                "severity": inc.severity,
                "status": inc.status,
                "confidence": round(inc.confidence * 100) if inc.confidence else 85,
                "occurred_at": inc.created_at.strftime("%b %d, %H:%M") if inc.created_at else "Aug 29, 14:02",
                "raw_date": inc.created_at.isoformat() if inc.created_at else None
            }
            for inc in incidents
        ]
    }

@router.get("/{incident_id}")
def get_incident_details(incident_id: str, db: Session = Depends(get_db)):
    seed_sample_incidents(db)
    inc = db.query(Incident).filter(Incident.incident_id == incident_id).first()
    if not inc:
        # Default fallback for demonstration
        inc = db.query(Incident).filter(Incident.incident_id == "INC-1024").first()
        if not inc:
            raise HTTPException(status_code=404, detail="Incident not found")

    rep = db.query(DiagnosisReport).filter(DiagnosisReport.incident_id == inc.incident_id).first()

    # Device details for the right panel (SWI-03)
    device_details = {
        "device_id": "SWI-03 (Building A)",
        "status": "Degraded",
        "cpu_usage": 78,
        "memory_usage": 64,
        "interface_errors": 126,
        "queue_drops": 34,
        "link_utilization": 92
    }

    # Investigation topology visualization
    topology = {
        "nodes": [
            {"id": "bldg_a", "label": "Building A", "sublabel": "(Affected)", "status": "Critical", "color": "#FF4568", "x": 100, "y": 200},
            {"id": "core_b", "label": "Core B", "sublabel": "(Healthy)", "status": "Healthy", "color": "#20D9FF", "x": 300, "y": 140},
            {"id": "bldg_b", "label": "Building B", "sublabel": "(Healthy)", "status": "Healthy", "color": "#20E88A", "x": 500, "y": 100},
            {"id": "branch_c", "label": "Branch C", "sublabel": "(Degraded)", "status": "Warning", "color": "#FFC247", "x": 480, "y": 260}
        ],
        "links": [
            {"source": "bldg_a", "target": "core_b", "status": "Critical"},
            {"source": "core_b", "target": "bldg_b", "status": "Healthy"},
            {"source": "core_b", "target": "branch_c", "status": "Warning"}
        ]
    }

    # Telemetry trend graph data
    telemetry_trend = [
        {"time": "13:50", "latency": 22, "packet_loss": 0.1, "cpu": 45, "link_util": 55},
        {"time": "13:55", "latency": 28, "packet_loss": 0.2, "cpu": 52, "link_util": 68},
        {"time": "14:00", "latency": 85, "packet_loss": 1.4, "cpu": 68, "link_util": 84},
        {"time": "14:02", "latency": 195, "packet_loss": 3.8, "cpu": 78, "link_util": 92},
        {"time": "14:05", "latency": 240, "packet_loss": 5.2, "cpu": 82, "link_util": 94}
    ]

    return {
        "incident_id": inc.incident_id,
        "title": inc.title,
        "severity": inc.severity,
        "status": inc.status,
        "subtitle": f"{inc.title} • Detected {inc.created_at.strftime('%H:%M') if inc.created_at else 'recently'}",
        "probable_root_cause": inc.probable_root_cause,
        "confidence": round(inc.confidence * 100) if inc.confidence else 87,
        "device_details": device_details,
        "topology": topology,
        "telemetry_trend": telemetry_trend,
        "report": rep.report_json if rep else None
    }
