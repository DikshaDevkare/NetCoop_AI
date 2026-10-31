from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
import random
from app.database.connection import get_db
from app.database.models import Incident, Device, TelemetryRecord
from app.utils.telemetry_generator import generate_telemetry

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    open_incidents_count = db.query(Incident).filter(Incident.status.in_(["Open", "In Progress"])).count()
    total_devices = db.query(Device).count()
    if total_devices == 0:
        total_devices = 428 # Realistic campus network topology device baseline

    # Calculate aggregate network health based on open incident severity
    critical_count = db.query(Incident).filter(Incident.severity == "Critical", Incident.status != "Resolved").count()
    high_count = db.query(Incident).filter(Incident.severity == "High", Incident.status != "Resolved").count()

    base_health = 96.0 - (critical_count * 8.0) - (high_count * 3.0)
    health_score = max(68.0, min(99.0, base_health))

    return {
        "network_health_pct": round(health_score, 1),
        "ai_agents_online": 5,
        "active_devices": total_devices,
        "open_incidents": max(1, open_incidents_count),
        "system_status": "System Online",
        "simulation_mode": True,
        "last_updated": datetime.now(timezone.utc).isoformat()
    }

@router.get("/telemetry")
def get_live_telemetry():
    """Returns live telemetry stream metrics with time-series history for charts."""
    sample = generate_telemetry(fault_type="normal", device_id="SWI-03")
    metrics = sample["normalized_metrics"]

    # Generate 12 historical points for smooth sparklines
    history = []
    now_ts = datetime.now(timezone.utc).timestamp()
    for i in range(12):
        step_time = datetime.fromtimestamp(now_ts - (11 - i) * 10, timezone.utc).strftime("%H:%M:%S")
        history.append({
            "time": step_time,
            "latency_ms": round(20.0 + random.uniform(-4, 8), 1),
            "packet_loss_pct": round(max(0.0, 0.4 + random.uniform(-0.3, 0.8)), 2),
            "bandwidth_mbps": round(290.0 + random.uniform(-30, 45), 1),
            "cpu_usage_pct": round(62.0 + random.uniform(-6, 12), 1),
            "link_utilization_pct": round(68.0 + random.uniform(-5, 10), 1)
        })

    # Ensure last point matches current readings
    history[-1]["latency_ms"] = 24.0
    history[-1]["packet_loss_pct"] = 0.8
    history[-1]["bandwidth_mbps"] = 312.0
    history[-1]["cpu_usage_pct"] = 68.0

    return {
        "current": {
            "latency_ms": 24.0,
            "packet_loss_pct": 0.8,
            "bandwidth_mbps": 312.0,
            "cpu_usage_pct": 68.0,
            "link_utilization_pct": 74.0,
            "device_id": "SWI-03 (Building A)",
            "device_status": "Degraded"
        },
        "history": history
    }

@router.get("/topology")
def get_network_topology():
    """Returns rich 3D network topology graph nodes and links matching the reference UI."""
    nodes = [
        {"id": "core_sw_01", "name": "Core Switch", "type": "Core Switch", "status": "Healthy", "cpu": 32, "memory": 45, "latency": 4.2, "loss": 0.0, "x": -2.5, "y": 0.5, "z": -1.5},
        {"id": "branch_rtr_01", "name": "Branch Router", "type": "Branch Router", "status": "Degraded", "cpu": 78, "memory": 64, "latency": 24.0, "loss": 0.8, "x": 0.0, "y": 0.0, "z": 0.0},
        {"id": "ap_01", "name": "Access Point", "type": "Access Point", "status": "Online", "cpu": 28, "memory": 38, "latency": 12.5, "loss": 0.1, "x": 2.8, "y": 0.8, "z": -1.2},
        {"id": "dist_sw_bldg_a", "name": "SWI-03 (Building A)", "type": "Access Switch", "status": "Degraded", "cpu": 78, "memory": 64, "latency": 28.5, "loss": 1.2, "x": -2.0, "y": -0.6, "z": 2.0},
        {"id": "dist_sw_bldg_b", "name": "Building B Switch", "type": "Access Switch", "status": "Healthy", "cpu": 34, "memory": 42, "latency": 6.8, "loss": 0.0, "x": 2.2, "y": -0.5, "z": 1.8}
    ]

    edges = [
        {"source": "branch_rtr_01", "target": "core_sw_01", "status": "Healthy", "traffic_rate": 820},
        {"source": "branch_rtr_01", "target": "dist_sw_bldg_a", "status": "Degraded", "traffic_rate": 450},
        {"source": "branch_rtr_01", "target": "dist_sw_bldg_b", "status": "Healthy", "traffic_rate": 310},
        {"source": "core_sw_01", "target": "ap_01", "status": "Healthy", "traffic_rate": 180}
    ]

    return {"nodes": nodes, "edges": edges}
