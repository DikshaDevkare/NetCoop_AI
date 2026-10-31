import random
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.protocols.validator import normalize_telemetry_metrics

DEVICE_CATALOG = [
    {"device_id": "CORE_SW_01", "device_type": "Core Switch", "hostname": "core-sw-01.campus.net", "network_segment": "Core Backbone"},
    {"device_id": "BRANCH_RTR_01", "device_type": "Branch Router", "hostname": "rtr-branch-01.campus.net", "network_segment": "Building A"},
    {"device_id": "SW_CAMPUS_01", "device_type": "Distribution Switch", "hostname": "sw-campus-01.campus.net", "network_segment": "Building A"},
    {"device_id": "SW_CAMPUS_02", "device_type": "Distribution Switch", "hostname": "sw-campus-02.campus.net", "network_segment": "Building B"},
    {"device_id": "SW_CAMPUS_03", "device_type": "Access Switch", "hostname": "sw-campus-03.campus.net", "network_segment": "Hostel Zone 1"},
    {"device_id": "SWI-03", "device_type": "Access Switch", "hostname": "swi-03.building-a.net", "network_segment": "Building A"},
    {"device_id": "AP_LECTURE_01", "device_type": "Access Point", "hostname": "ap-lecture-01.campus.net", "network_segment": "Lecture Complex"},
    {"device_id": "AP_HOSTEL_02", "device_type": "Access Point", "hostname": "ap-hostel-02.campus.net", "network_segment": "Hostel Zone 2"},
    {"device_id": "SRV_DNS_DHCP_01", "device_type": "Core Server", "hostname": "dns-dhcp-01.campus.net", "network_segment": "Datacenter"},
    {"device_id": "GATEWAY_EDGE_01", "device_type": "Edge Gateway", "hostname": "edge-gw-01.campus.net", "network_segment": "Edge DMZ"}
]

def generate_telemetry(fault_type: str = "normal", seed: Optional[int] = None, device_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Preserves organization provided implementation and extends with all campus fault scenarios.
    """
    if seed is not None:
        random.seed(seed)

    selected_dev = None
    if device_id:
        for dev in DEVICE_CATALOG:
            if dev["device_id"] == device_id:
                selected_dev = dev
                break
    if not selected_dev:
        selected_dev = random.choice(DEVICE_CATALOG)

    chosen_device_id = selected_dev["device_id"]

    data = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "device_id": chosen_device_id,
        "device_type": selected_dev["device_type"],
        "network_segment": selected_dev["network_segment"],
        "metrics": {}
    }

    normalized_fault = fault_type.lower().strip().replace(" ", "_")

    # Original Organizer Scenarios preserved:
    if normalized_fault == "latency_spike":
        data["metrics"] = {
            "cpu_utilization_pct": round(random.uniform(40, 70), 2),
            "link_utilization_pct": round(random.uniform(60, 85), 2),
            "packet_loss_pct": round(random.uniform(0.1, 1.5), 2),
            "latency_ms": round(random.uniform(150, 400), 2),
            "jitter_ms": round(random.uniform(30, 80), 2),
            "queue_drops": random.randint(0, 50),
            "throughput_mbps": round(random.uniform(180, 420), 2),
            "dns_resolution_time_ms": round(random.uniform(15, 35), 2)
        }
        data["status"] = "Warning"

    elif normalized_fault == "hardware_failure":
        data["metrics"] = {
            "cpu_utilization_pct": 99.9,
            "link_utilization_pct": 100.0,
            "packet_loss_pct": round(random.uniform(15, 30), 2),
            "latency_ms": round(random.uniform(500, 1000), 2),
            "queue_drops": random.randint(5000, 15000),
            "interface_errors": random.randint(100, 500),
            "throughput_mbps": round(random.uniform(5, 45), 2),
            "memory_utilization_pct": round(random.uniform(94, 99), 2)
        }
        data["status"] = "Critical"

    elif normalized_fault in ("congestion", "network_congestion"):
        data["metrics"] = {
            "cpu_utilization_pct": round(random.uniform(70, 92), 2),
            "link_utilization_pct": round(random.uniform(88, 98), 2),
            "packet_loss_pct": round(random.uniform(2.5, 7.5), 2),
            "latency_ms": round(random.uniform(120, 290), 2),
            "jitter_ms": round(random.uniform(25, 65), 2),
            "queue_drops": random.randint(450, 2400),
            "interface_errors": random.randint(10, 80),
            "throughput_mbps": round(random.uniform(750, 960), 2)
        }
        data["status"] = "Degraded"

    elif normalized_fault in ("interface_fault", "link_interface_failure", "link_failure"):
        data["metrics"] = {
            "cpu_utilization_pct": round(random.uniform(30, 55), 2),
            "link_utilization_pct": round(random.uniform(40, 75), 2),
            "packet_loss_pct": round(random.uniform(6.0, 22.0), 2),
            "latency_ms": round(random.uniform(80, 240), 2),
            "jitter_ms": round(random.uniform(20, 60), 2),
            "queue_drops": random.randint(20, 150),
            "interface_errors": random.randint(250, 1400),
            "throughput_mbps": round(random.uniform(60, 250), 2)
        }
        data["status"] = "Critical"

    elif normalized_fault in ("dns_dhcp_failure", "dns_failure", "dhcp_failure"):
        data["metrics"] = {
            "cpu_utilization_pct": round(random.uniform(25, 50), 2),
            "link_utilization_pct": round(random.uniform(20, 45), 2),
            "packet_loss_pct": round(random.uniform(0.5, 2.0), 2),
            "latency_ms": round(random.uniform(20, 45), 2),
            "jitter_ms": round(random.uniform(2, 10), 2),
            "queue_drops": 0,
            "dns_resolution_time_ms": round(random.uniform(1800, 4500), 2),
            "dns_error_rate_pct": round(random.uniform(45.0, 95.0), 2),
            "dhcp_ack_latency_ms": round(random.uniform(2500, 6000), 2)
        }
        data["status"] = "Degraded"

    elif normalized_fault in ("device_overload", "cpu_overload"):
        data["metrics"] = {
            "cpu_utilization_pct": round(random.uniform(92, 99.5), 2),
            "memory_utilization_pct": round(random.uniform(88, 97.5), 2),
            "link_utilization_pct": round(random.uniform(65, 85), 2),
            "packet_loss_pct": round(random.uniform(3.0, 10.0), 2),
            "latency_ms": round(random.uniform(110, 320), 2),
            "jitter_ms": round(random.uniform(20, 50), 2),
            "queue_drops": random.randint(300, 1800),
            "interface_errors": random.randint(20, 90)
        }
        data["status"] = "Critical"

    elif normalized_fault in ("weak_wifi", "wifi_signal_issue"):
        data["metrics"] = {
            "cpu_utilization_pct": round(random.uniform(20, 40), 2),
            "link_utilization_pct": round(random.uniform(30, 60), 2),
            "packet_loss_pct": round(random.uniform(4.0, 16.0), 2),
            "latency_ms": round(random.uniform(65, 180), 2),
            "jitter_ms": round(random.uniform(25, 80), 2),
            "queue_drops": random.randint(10, 80),
            "wifi_rssi_dbm": round(random.uniform(-89.0, -78.0), 1),
            "wifi_snr_db": round(random.uniform(4.0, 12.0), 1),
            "wifi_retrans_pct": round(random.uniform(32.0, 75.0), 2)
        }
        data["status"] = "Warning"

    else: # normal
        data["metrics"] = {
            "cpu_utilization_pct": round(random.uniform(10, 35), 2),
            "link_utilization_pct": round(random.uniform(20, 50), 2),
            "packet_loss_pct": 0.0,
            "latency_ms": round(random.uniform(5, 20), 2),
            "jitter_ms": round(random.uniform(1, 5), 2),
            "queue_drops": 0,
            "interface_errors": 0,
            "throughput_mbps": round(random.uniform(450, 850), 2),
            "dns_resolution_time_ms": round(random.uniform(8, 22), 2),
            "dns_error_rate_pct": 0.0,
            "dhcp_ack_latency_ms": round(random.uniform(15, 60), 2),
            "wifi_rssi_dbm": round(random.uniform(-55.0, -40.0), 1),
            "wifi_snr_db": round(random.uniform(25.0, 42.0), 1),
            "wifi_retrans_pct": round(random.uniform(0.5, 3.5), 2)
        }
        data["status"] = "Healthy"

    # Add normalized metrics alongside
    data["normalized_metrics"] = normalize_telemetry_metrics(data["metrics"])
    return data

def generate_telemetry_series(fault_type: str = "normal", count: int = 15, seed: Optional[int] = 42, device_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Generates a chronological time-series of telemetry records for temporal trend analysis."""
    if seed is not None:
        random.seed(seed)
    
    series = []
    base_dev = device_id or "SWI-03"
    for i in range(count):
        rec = generate_telemetry(fault_type=fault_type, seed=(seed + i) if seed else None, device_id=base_dev)
        # Shift timestamps backwards in 15-second increments
        series.append(rec)
    return series
