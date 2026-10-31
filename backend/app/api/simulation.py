from fastapi import APIRouter, Query, Body
from typing import Dict, Any, Optional
from app.utils.telemetry_generator import generate_telemetry, generate_telemetry_series

router = APIRouter(prefix="/simulation", tags=["Simulation"])

SCENARIO_LIST = [
    {
        "id": "network_congestion",
        "title": "Network Congestion",
        "icon": "Activity",
        "description": "High throughput demands exceeding uplink buffer capacity causing queue drops and high RTT.",
        "severity": "High",
        "recommended_device": "SWI-03"
    },
    {
        "id": "link_interface_failure",
        "title": "Link / Interface Failure",
        "icon": "AlertTriangle",
        "description": "Physical link degradation or CRC errors causing intermittent packet loss and port flapping.",
        "severity": "Critical",
        "recommended_device": "SW_CAMPUS_01"
    },
    {
        "id": "dns_dhcp_failure",
        "title": "DNS / DHCP Failure",
        "icon": "Globe",
        "description": "Critical service resolver timeout preventing client IP address acquisition and domain lookups.",
        "severity": "High",
        "recommended_device": "SRV_DNS_DHCP_01"
    },
    {
        "id": "device_overload",
        "title": "Device Overload",
        "icon": "Cpu",
        "description": "Control plane exhaustion exceeding 95% CPU and memory saturation under heavy routing loops.",
        "severity": "Critical",
        "recommended_device": "BRANCH_RTR_01"
    },
    {
        "id": "wifi_signal_issue",
        "title": "Wi-Fi Signal Issue",
        "icon": "Wifi",
        "description": "Sub-optimal RSSI, low signal-to-noise ratio, and excessive 802.11 frame retransmissions.",
        "severity": "Warning",
        "recommended_device": "AP_HOSTEL_02"
    },
    {
        "id": "custom_scenario",
        "title": "Custom Scenario",
        "icon": "Sliders",
        "description": "Configure custom latency, jitter, loss and queue drops or upload telemetry captures.",
        "severity": "Variable",
        "recommended_device": "CUSTOM"
    }
]

@router.get("/scenarios")
def get_scenarios():
    return {
        "scenarios": SCENARIO_LIST,
        "sample_files": [
            {"name": "site-a_telemetry.csv", "size": "2.4 MB", "status": "valid"},
            {"name": "interfaces.json", "size": "532 KB", "status": "valid"},
            {"name": "topology.json", "size": "1.1 MB", "status": "valid"}
        ]
    }

@router.post("/generate")
def generate_scenario_telemetry(payload: Dict[str, Any] = Body(...)):
    scenario = payload.get("scenario", "network_congestion")
    seed = payload.get("seed")
    device_id = payload.get("device_id")

    single = generate_telemetry(fault_type=scenario, seed=seed, device_id=device_id)
    series = generate_telemetry_series(fault_type=scenario, count=10, seed=seed, device_id=device_id)

    return {
        "scenario": scenario,
        "current_telemetry": single,
        "time_series": series
    }
