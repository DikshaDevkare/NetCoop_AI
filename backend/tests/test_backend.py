import os
import pytest
import httpx
from app.main import app
from app.protocols.validator import validate_agent_message, normalize_telemetry_metrics
from app.utils.telemetry_generator import generate_telemetry
from app.orchestrator.orchestrator import DiagnosticOrchestrator

@pytest.fixture
async def async_client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as c:
        yield c

@pytest.mark.anyio
async def test_api_health(async_client):
    res = await async_client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
    assert data["active_models"] == 4

@pytest.mark.anyio
async def test_dashboard_stats(async_client):
    res = await async_client.get("/api/dashboard/stats")
    assert res.status_code == 200
    data = res.json()
    assert "network_health_pct" in data
    assert data["ai_agents_online"] == 5

@pytest.mark.anyio
async def test_dashboard_telemetry(async_client):
    res = await async_client.get("/api/dashboard/telemetry")
    assert res.status_code == 200
    data = res.json()
    assert "current" in data
    assert "history" in data
    assert len(data["history"]) >= 5

@pytest.mark.anyio
async def test_user_registration_and_login(async_client):
    email = f"netops_test_{os.urandom(4).hex()}@campus.edu"
    reg_payload = {
        "name": "Alex Mercer",
        "email": email,
        "password": "Password123!",
        "organization": "Campus IT",
        "role": "Senior Network Engineer"
    }
    reg_res = await async_client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 200
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == email

    # Login
    login_payload = {"email": email, "password": "Password123!"}
    login_res = await async_client.post("/api/auth/login", json=login_payload)
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

def test_telemetry_normalization():
    raw = {
        "latency": "24.5ms",
        "cpu_utilization_pct": 78.2,
        "packetLoss": 1.2,
        "bandwidth_utilization": 88.0,
        "queue_drops": 34
    }
    norm = normalize_telemetry_metrics(raw)
    assert norm["latency_ms"] == 24.5
    assert norm["cpu_usage_pct"] == 78.2
    assert norm["packet_loss_pct"] == 1.2
    assert norm["link_utilization_pct"] == 88.0
    assert norm["queue_drops"] == 34.0

def test_protocol_message_validation():
    valid_msg = {
        "message_id": "MSG-TEST-01",
        "incident_id": "INC-TEST",
        "sender": "performance_agent",
        "receiver": "fault_correlation_agent",
        "message_type": "diagnostic_finding",
        "schema_version": "1.0",
        "payload": {
            "finding": "high_network_latency",
            "metric": "latency_ms",
            "value": 240,
            "unit": "ms"
        }
    }
    is_valid, errors, _ = validate_agent_message(valid_msg)
    assert is_valid is True
    assert len(errors) == 0

    invalid_msg = {
        "sender": "unknown_actor",
        "payload": "invalid_string_not_dict"
    }
    is_invalid, errs, _ = validate_agent_message(invalid_msg)
    assert is_invalid is False
    assert len(errs) > 0

@pytest.mark.anyio
async def test_interoperability_api_endpoint(async_client):
    payload = {
        "message_id": "msg-7042",
        "sender": "orchestrator",
        "receiver": "performance_agent",
        "message_type": "diagnosis_request",
        "schema_version": "1.0",
        "payload": {
            "incident_id": "INC-1024",
            "telemetry_window": "15m"
        }
    }
    res = await async_client.post("/api/interoperability/validate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["is_valid"] is True
    assert data["checks"]["schema_valid"] is True

@pytest.mark.anyio
async def test_models_status_and_metrics(async_client):
    res = await async_client.get("/api/models/status")
    assert res.status_code == 200
    data = res.json()
    assert data["all_ready"] is True
    assert data["total_models"] == 4

    metrics_res = await async_client.get("/api/models/metrics")
    assert metrics_res.status_code == 200
    m_data = metrics_res.json()
    assert "models" in m_data
    assert "isolation_forest" in m_data["models"]
    assert "xgboost_fault_classifier" in m_data["models"]

def test_end_to_end_orchestrator_diagnosis():
    orchestrator = DiagnosticOrchestrator()
    sample = generate_telemetry(fault_type="congestion", device_id="SWI-03")
    
    result = orchestrator.run_diagnosis(
        telemetry_data=sample,
        historical_records=[sample, sample],
        incident_id="INC-TEST-E2E",
        scenario_name="network_congestion"
    )

    assert result["status"] == "completed"
    assert result["incident_id"] == "INC-TEST-E2E"
    assert len(result["timeline"]) >= 5
    assert len(result["messages"]) >= 4
    assert len(result["findings"]) >= 3
    assert "ml_results" in result
    assert "report" in result
    assert result["report"]["confidence"] >= 0.50
    assert "congestion" in result["report"]["root_cause"].lower() or "swi-03" in result["report"]["root_cause"].lower()
