from typing import Any, Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class AgentMessagePayload(BaseModel):
    finding: Optional[str] = None
    severity: Optional[str] = "medium" # low, medium, high, critical
    metric: Optional[str] = None
    value: Optional[float] = None
    unit: Optional[str] = None
    device_id: Optional[str] = None
    evidence: Optional[List[str]] = Field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class AgentMessageSchema(BaseModel):
    message_id: str
    incident_id: Optional[str] = None
    sender: str
    receiver: str
    message_type: str # diagnostic_finding, telemetry_query, correlation_result, recommendation_report, handshake
    schema_version: str = "1.0"
    timestamp: Optional[str] = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    payload: Dict[str, Any]

class TelemetryMetricSchema(BaseModel):
    latency_ms: Optional[float] = None
    packet_loss_pct: Optional[float] = None
    jitter_ms: Optional[float] = None
    cpu_usage_pct: Optional[float] = None
    memory_usage_pct: Optional[float] = None
    link_utilization_pct: Optional[float] = None
    queue_drops: Optional[int] = None
    interface_errors: Optional[int] = None
    throughput_mbps: Optional[float] = None
    dns_resolution_time_ms: Optional[float] = None
    dns_error_rate_pct: Optional[float] = None
    dhcp_ack_latency_ms: Optional[float] = None
    wifi_rssi_dbm: Optional[float] = None
    wifi_snr_db: Optional[float] = None
    wifi_retrans_pct: Optional[float] = None

class TelemetryIngestSchema(BaseModel):
    device_id: str
    timestamp: Optional[str] = None
    status: Optional[str] = "Healthy"
    metrics: Dict[str, Any]

class TelemetryUploadBatch(BaseModel):
    incident_id: Optional[str] = None
    records: List[TelemetryIngestSchema]
