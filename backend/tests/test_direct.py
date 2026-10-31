import os
from app.main import health_check
from app.database.connection import SessionLocal
from app.api.dashboard import get_dashboard_stats, get_live_telemetry, get_network_topology
from app.api.auth import register, login, RegisterRequest, LoginRequest
from app.api.incidents import list_incidents, get_incident_details
from app.api.agents import get_agents_status, get_agent_messages, get_execution_timeline
from app.api.interoperability import validate_protocol_message, send_test_message, get_protocol_schemas
from app.api.models import get_models_status, get_model_metrics
from app.api.simulation import get_scenarios, generate_scenario_telemetry
from app.orchestrator.orchestrator import DiagnosticOrchestrator
from app.utils.telemetry_generator import generate_telemetry
from app.protocols.validator import normalize_telemetry_metrics, validate_agent_message

def test_all_direct():
    print("Testing health check...")
    h = health_check()
    assert h["status"] == "healthy"
    print("Health check OK:", h["status"])

    db = SessionLocal()
    try:
        print("Testing dashboard stats...")
        stats = get_dashboard_stats(db=db)
        assert stats["ai_agents_online"] == 5
        print("Dashboard stats OK:", stats["network_health_pct"])

        print("Testing live telemetry...")
        telem = get_live_telemetry()
        assert "current" in telem
        print("Live telemetry OK:", telem["current"]["latency_ms"], "ms")

        print("Testing topology...")
        topo = get_network_topology()
        assert len(topo["nodes"]) >= 4
        print("Topology OK:", len(topo["nodes"]), "nodes")

        print("Testing incidents...")
        incs = list_incidents(db=db)
        assert len(incs["incidents"]) >= 1
        print("Incidents list OK:", len(incs["incidents"]), "incidents found")

        inc_det = get_incident_details("INC-1024", db=db)
        assert inc_det["incident_id"] == "INC-1024"
        print("Incident details OK:", inc_det["title"])

        print("Testing agents status...")
        agents = get_agents_status()
        assert len(agents["agents"]) == 5
        print("Agents status OK:", len(agents["agents"]), "agents online")

        print("Testing agent messages...")
        msgs = get_agent_messages("INC-1024", db=db)
        assert len(msgs) >= 3
        print("Agent messages OK:", len(msgs), "messages logged")

        print("Testing model status & metrics...")
        m_status = get_models_status()
        assert m_status["all_ready"] is True
        print("Models status OK: All 4 models ready")

        m_metrics = get_model_metrics(db=db)
        assert "models" in m_metrics
        print("Model metrics OK:", list(m_metrics["models"].keys()))

        print("Testing user auth...")
        test_email = f"alex_{os.urandom(4).hex()}@campus.edu"
        reg = register(RegisterRequest(name="Alex Test", email=test_email, password="SecretPassword123!"), db=db)
        assert "access_token" in reg
        log = login(LoginRequest(email=test_email, password="SecretPassword123!"), db=db)
        assert "access_token" in log
        print("Auth registration and login OK!")

        print("Testing interoperability validation...")
        val_res = validate_protocol_message({
            "message_id": "MSG-TEST",
            "sender": "performance_agent",
            "receiver": "fault_correlation_agent",
            "message_type": "diagnostic_finding",
            "schema_version": "1.0",
            "payload": {"finding": "high_latency", "metric": "latency_ms", "value": 240, "unit": "ms"}
        })
        assert val_res["is_valid"] is True
        print("Interoperability validation OK!")

        print("Testing complete end-to-end multi-agent orchestrator diagnosis...")
        orchestrator = DiagnosticOrchestrator()
        sample_telem = generate_telemetry(fault_type="congestion", device_id="SWI-03")
        diag_res = orchestrator.run_diagnosis(
            telemetry_data=sample_telem,
            historical_records=[sample_telem],
            incident_id="INC-AUTO-TEST",
            scenario_name="network_congestion"
        )
        assert diag_res["status"] == "completed"
        assert len(diag_res["timeline"]) >= 5
        assert len(diag_res["messages"]) >= 4
        assert diag_res["report"]["confidence"] >= 0.5
        print("Multi-agent diagnosis OK! Root cause:", diag_res["report"]["root_cause"])
        print("\nALL BACKEND UNIT & INTEGRATION TESTS PASSED PERFECTLY!")
    finally:
        db.close()

if __name__ == "__main__":
    test_all_direct()
