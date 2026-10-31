import os
import random
import numpy as np
import pandas as pd
from typing import Tuple, Dict, Any, List

FEATURE_NAMES = [
    "latency_ms",
    "packet_loss_pct",
    "jitter_ms",
    "cpu_usage_pct",
    "memory_usage_pct",
    "link_utilization_pct",
    "queue_drops",
    "interface_errors",
    "dns_resolution_time_ms",
    "dns_error_rate_pct",
    "dhcp_ack_latency_ms",
    "wifi_rssi_dbm",
    "wifi_snr_db",
    "wifi_retrans_pct"
]

SCENARIOS = [
    "normal",
    "congestion",
    "latency_spike",
    "hardware_failure",
    "weak_wifi",
    "interface_fault",
    "dns_dhcp_failure"
]

INFRA_CLASSES = [
    "normal",
    "cpu_overload",
    "memory_pressure",
    "interface_failure",
    "hardware_failure",
    "queue_congestion"
]

HEALTH_CLASSES = [
    "Healthy",
    "Warning",
    "Critical"
]

def generate_synthetic_record(scenario: str, incident_id: str, seed: int = None) -> Dict[str, Any]:
    if seed is not None:
        np.random.seed(seed)
        random.seed(seed)
        
    row = {
        "incident_id": incident_id,
        "scenario": scenario,
        "latency_ms": 12.0 + np.random.normal(0, 3.0),
        "packet_loss_pct": max(0.0, float(np.random.normal(0.0, 0.05))),
        "jitter_ms": max(0.5, 2.5 + np.random.normal(0, 0.8)),
        "cpu_usage_pct": max(5.0, min(100.0, 22.0 + np.random.normal(0, 6.0))),
        "memory_usage_pct": max(10.0, min(100.0, 35.0 + np.random.normal(0, 7.0))),
        "link_utilization_pct": max(5.0, min(100.0, 32.0 + np.random.normal(0, 8.0))),
        "queue_drops": 0,
        "interface_errors": 0,
        "dns_resolution_time_ms": max(5.0, 15.0 + np.random.normal(0, 4.0)),
        "dns_error_rate_pct": 0.0,
        "dhcp_ack_latency_ms": max(10.0, 30.0 + np.random.normal(0, 8.0)),
        "wifi_rssi_dbm": -48.0 + np.random.normal(0, 4.0),
        "wifi_snr_db": 34.0 + np.random.normal(0, 3.0),
        "wifi_retrans_pct": max(0.1, 1.8 + np.random.normal(0, 0.6)),
        "infra_condition": "normal",
        "health_state": "Healthy",
        "is_anomaly": 0
    }

    if scenario == "congestion":
        row["link_utilization_pct"] = np.random.uniform(88.0, 99.0)
        row["queue_drops"] = int(np.random.uniform(400, 3200))
        row["latency_ms"] = np.random.uniform(110.0, 280.0)
        row["packet_loss_pct"] = np.random.uniform(2.0, 7.5)
        row["jitter_ms"] = np.random.uniform(25.0, 65.0)
        row["cpu_usage_pct"] = np.random.uniform(70.0, 90.0)
        row["infra_condition"] = "queue_congestion"
        row["health_state"] = "Warning"
        row["is_anomaly"] = 1

    elif scenario == "latency_spike":
        row["latency_ms"] = np.random.uniform(180.0, 450.0)
        row["jitter_ms"] = np.random.uniform(35.0, 95.0)
        row["link_utilization_pct"] = np.random.uniform(60.0, 85.0)
        row["packet_loss_pct"] = np.random.uniform(0.2, 1.8)
        row["queue_drops"] = int(np.random.uniform(5, 60))
        row["cpu_usage_pct"] = np.random.uniform(40.0, 70.0)
        row["infra_condition"] = "normal"
        row["health_state"] = "Warning"
        row["is_anomaly"] = 1

    elif scenario == "hardware_failure":
        row["cpu_usage_pct"] = np.random.uniform(97.0, 100.0)
        row["memory_usage_pct"] = np.random.uniform(94.0, 99.9)
        row["link_utilization_pct"] = 100.0
        row["packet_loss_pct"] = np.random.uniform(16.0, 35.0)
        row["latency_ms"] = np.random.uniform(520.0, 1100.0)
        row["queue_drops"] = int(np.random.uniform(6000, 18000))
        row["interface_errors"] = int(np.random.uniform(150, 700))
        row["infra_condition"] = "hardware_failure"
        row["health_state"] = "Critical"
        row["is_anomaly"] = 1

    elif scenario == "weak_wifi":
        row["wifi_rssi_dbm"] = np.random.uniform(-89.0, -78.0)
        row["wifi_snr_db"] = np.random.uniform(3.0, 11.0)
        row["wifi_retrans_pct"] = np.random.uniform(35.0, 80.0)
        row["packet_loss_pct"] = np.random.uniform(4.0, 15.0)
        row["latency_ms"] = np.random.uniform(70.0, 190.0)
        row["jitter_ms"] = np.random.uniform(30.0, 85.0)
        row["infra_condition"] = "normal"
        row["health_state"] = "Warning"
        row["is_anomaly"] = 1

    elif scenario == "interface_fault":
        row["interface_errors"] = int(np.random.uniform(300, 1800))
        row["packet_loss_pct"] = np.random.uniform(6.0, 24.0)
        row["latency_ms"] = np.random.uniform(75.0, 250.0)
        row["queue_drops"] = int(np.random.uniform(15, 120))
        row["infra_condition"] = "interface_failure"
        row["health_state"] = "Critical"
        row["is_anomaly"] = 1

    elif scenario == "dns_dhcp_failure":
        row["dns_resolution_time_ms"] = np.random.uniform(1900.0, 4800.0)
        row["dns_error_rate_pct"] = np.random.uniform(50.0, 98.0)
        row["dhcp_ack_latency_ms"] = np.random.uniform(2800.0, 6500.0)
        row["packet_loss_pct"] = np.random.uniform(0.5, 2.5)
        row["infra_condition"] = "normal"
        row["health_state"] = "Warning"
        row["is_anomaly"] = 1

    # Clamp ranges safely
    row["latency_ms"] = round(float(max(1.0, row["latency_ms"])), 2)
    row["packet_loss_pct"] = round(float(max(0.0, min(100.0, row["packet_loss_pct"]))), 2)
    row["jitter_ms"] = round(float(max(0.1, row["jitter_ms"])), 2)
    row["cpu_usage_pct"] = round(float(max(0.0, min(100.0, row["cpu_usage_pct"]))), 2)
    row["memory_usage_pct"] = round(float(max(0.0, min(100.0, row["memory_usage_pct"]))), 2)
    row["link_utilization_pct"] = round(float(max(0.0, min(100.0, row["link_utilization_pct"]))), 2)
    row["dns_resolution_time_ms"] = round(float(row["dns_resolution_time_ms"]), 2)
    row["dns_error_rate_pct"] = round(float(min(100.0, row["dns_error_rate_pct"])), 2)
    row["dhcp_ack_latency_ms"] = round(float(row["dhcp_ack_latency_ms"]), 2)
    row["wifi_rssi_dbm"] = round(float(row["wifi_rssi_dbm"]), 1)
    row["wifi_snr_db"] = round(float(row["wifi_snr_db"]), 1)
    row["wifi_retrans_pct"] = round(float(min(100.0, row["wifi_retrans_pct"])), 2)

    return row

def generate_synthetic_dataset(num_incidents: int = 350, records_per_incident: int = 10, base_seed: int = 42) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Generates incident-wise split: 70% train incidents, 15% val incidents, 15% test incidents.
    No incident records leak across splits.
    """
    incidents = []
    rng = np.random.RandomState(base_seed)

    for i in range(num_incidents):
        inc_id = f"INC-SIM-{i+1:04d}"
        scenario = rng.choice(SCENARIOS)
        # Give normal higher prior weight to simulate realistic background traffic
        if rng.rand() < 0.35:
            scenario = "normal"
            
        for r in range(records_per_incident):
            rec = generate_synthetic_record(scenario=scenario, incident_id=inc_id, seed=base_seed + i * 100 + r)
            incidents.append(rec)

    df = pd.DataFrame(incidents)

    unique_incidents = list(df["incident_id"].unique())
    rng.shuffle(unique_incidents)

    n_inc = len(unique_incidents)
    n_train = int(n_inc * 0.70)
    n_val = int(n_inc * 0.15)

    train_ids = set(unique_incidents[:n_train])
    val_ids = set(unique_incidents[n_train:n_train + n_val])
    test_ids = set(unique_incidents[n_train + n_val:])

    train_df = df[df["incident_id"].isin(train_ids)].reset_index(drop=True)
    val_df = df[df["incident_id"].isin(val_ids)].reset_index(drop=True)
    test_df = df[df["incident_id"].isin(test_ids)].reset_index(drop=True)

    return train_df, val_df, test_df
