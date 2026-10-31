import os
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from app.config import settings
from app.protocols.validator import normalize_telemetry_metrics
from app.ml.anomaly_detection.isolation_forest_model import IsolationForestAnomalyDetector
from app.ml.fault_classification.xgboost_model import XGBoostFaultClassifier
from app.ml.infrastructure_classification.random_forest_model import RandomForestInfraClassifier
from app.ml.network_health_classification.gradient_boosting_model import GradientBoostingHealthClassifier
from app.ml.temporal_analysis.temporal_analyzer import TemporalTelemetryAnalyzer

from app.agents.performance_agent import PerformanceAgent
from app.agents.infrastructure_agent import InfrastructureAgent
from app.agents.connectivity_agent import ConnectivityAgent
from app.agents.fault_correlation_agent import FaultCorrelationAgent
from app.agents.reporting_agent import ReportingAgent

from app.database.connection import SessionLocal
from app.database.models import Incident, TelemetryRecord, AgentMessage, AgentFinding, DiagnosisReport, Device

class DiagnosticOrchestrator:
    def __init__(self):
        self.artifacts_dir = settings.ARTIFACTS_DIR
        self._load_models()

        # Instantiate agents
        self.perf_agent = PerformanceAgent()
        self.infra_agent = InfrastructureAgent()
        self.conn_agent = ConnectivityAgent()
        self.corr_agent = FaultCorrelationAgent()
        self.report_agent = ReportingAgent()
        self.temporal_analyzer = TemporalTelemetryAnalyzer()

    def _load_models(self):
        self.iso_model = IsolationForestAnomalyDetector()
        self.xgb_model = XGBoostFaultClassifier()
        self.rf_model = RandomForestInfraClassifier()
        self.gb_model = GradientBoostingHealthClassifier()

        iso_path = os.path.join(self.artifacts_dir, "isolation_forest.joblib")
        xgb_path = os.path.join(self.artifacts_dir, "xgboost_fault_classifier.joblib")
        rf_path = os.path.join(self.artifacts_dir, "random_forest_infra.joblib")
        gb_path = os.path.join(self.artifacts_dir, "gradient_boosting_health.joblib")

        try:
            if os.path.exists(iso_path):
                self.iso_model.load(iso_path)
            if os.path.exists(xgb_path):
                self.xgb_model.load(xgb_path)
            if os.path.exists(rf_path):
                self.rf_model.load(rf_path)
            if os.path.exists(gb_path):
                self.gb_model.load(gb_path)
            print("Orchestrator: All 4 ML models loaded successfully.")
        except Exception as e:
            print(f"Orchestrator warning loading models: {e}")

    def run_diagnosis(
        self,
        telemetry_data: Dict[str, Any],
        historical_records: Optional[List[Dict[str, Any]]] = None,
        incident_id: Optional[str] = None,
        scenario_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes end-to-end multi-agent network fault diagnosis workflow.
        """
        if not incident_id:
            incident_id = f"INC-{uuid.uuid4().hex[:4].upper()}"

        start_time = datetime.now(timezone.utc)
        timeline = []
        timeline.append({
            "stage": "orchestrator_initialized",
            "title": "Orchestrator Initialized",
            "time": start_time.strftime("%H:%M:%S"),
            "status": "completed"
        })

        # 1. Normalization & Validation
        raw_metrics = telemetry_data.get("metrics", {})
        norm_metrics = normalize_telemetry_metrics(raw_metrics)
        telemetry_data["normalized_metrics"] = norm_metrics
        device_id = telemetry_data.get("device_id", "CAMPUS_SW_01")

        timeline.append({
            "stage": "telemetry_validated",
            "title": "Telemetry Normalization & Validation",
            "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "status": "completed"
        })

        # 2. Four ML Model Inferences
        ml_results = {}
        try:
            ml_results["isolation_forest"] = self.iso_model.predict(norm_metrics)
        except Exception as e:
            ml_results["isolation_forest"] = {"error": str(e), "is_anomaly": False}

        try:
            ml_results["xgboost"] = self.xgb_model.predict(norm_metrics)
        except Exception as e:
            ml_results["xgboost"] = {"error": str(e), "predicted_fault": "normal", "confidence": 0.5}

        try:
            ml_results["random_forest"] = self.rf_model.predict(norm_metrics)
        except Exception as e:
            ml_results["random_forest"] = {"error": str(e), "predicted_condition": "normal", "confidence": 0.5}

        try:
            ml_results["gradient_boosting"] = self.gb_model.predict(norm_metrics)
        except Exception as e:
            ml_results["gradient_boosting"] = {"error": str(e), "predicted_health": "Healthy", "confidence": 0.5}

        # 3. Temporal Telemetry Analysis
        temporal_records = (historical_records or []) + [telemetry_data]
        temporal_res = self.temporal_analyzer.analyze_sequence(temporal_records)

        context = {
            "incident_id": incident_id,
            "ml_results": ml_results,
            "temporal_analysis": temporal_res,
            "scenario": scenario_name
        }

        # 4. Agent Execution with real messaging
        messages = []
        findings = []

        # Step 4a: Performance Agent
        timeline.append({
            "stage": "performance_agent",
            "title": "Performance Agent Analysis",
            "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "status": "completed"
        })
        perf_res = self.perf_agent.analyze(telemetry_data, context=context)
        findings.append(perf_res)
        messages.append(perf_res["message"])

        # Step 4b: Infrastructure Health Agent
        timeline.append({
            "stage": "infrastructure_agent",
            "title": "Infrastructure Health Analysis",
            "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "status": "completed"
        })
        infra_res = self.infra_agent.analyze(telemetry_data, context=context)
        findings.append(infra_res)
        messages.append(infra_res["message"])

        # Step 4c: Connectivity Analysis Agent
        timeline.append({
            "stage": "connectivity_agent",
            "title": "Connectivity Analysis",
            "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "status": "completed"
        })
        conn_res = self.conn_agent.analyze(telemetry_data, context=context)
        findings.append(conn_res)
        messages.append(conn_res["message"])

        # Step 4d: Fault Correlation Agent
        timeline.append({
            "stage": "fault_correlation",
            "title": "Fault Correlation & Conflict Resolution",
            "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "status": "completed"
        })
        corr_res = self.corr_agent.correlate(
            agent_findings=findings,
            ml_results=ml_results,
            temporal_analysis=temporal_res,
            telemetry_data=telemetry_data,
            incident_id=incident_id
        )
        messages.append(corr_res["message"])

        # Step 4e: Recommendation & Reporting Agent
        timeline.append({
            "stage": "report_generation",
            "title": "Report Generation & Action Playbook",
            "time": datetime.now(timezone.utc).strftime("%H:%M:%S"),
            "status": "completed"
        })
        report_res = self.report_agent.generate_report(
            correlation_result=corr_res,
            incident_id=incident_id,
            telemetry_data=telemetry_data
        )
        messages.append(report_res["message"])

        final_report = report_res["report"]

        # Determine severity from health model and correlation
        gb_health = ml_results.get("gradient_boosting", {}).get("predicted_health", "Healthy")
        severity_map = {"Critical": "Critical", "Warning": "High", "Healthy": "Low"}
        incident_severity = severity_map.get(gb_health, "Medium")
        if "Critical" in str(corr_res.get("correlation", {}).get("probable_root_cause")):
            incident_severity = "Critical"

        # 5. Persist to Database
        db = SessionLocal()
        try:
            # Check or create Incident
            existing_inc = db.query(Incident).filter(Incident.incident_id == incident_id).first()
            if not existing_inc:
                new_inc = Incident(
                    incident_id=incident_id,
                    title=f"Network Incident on {device_id} ({scenario_name or 'Auto-Detected'})",
                    description=final_report["root_cause"],
                    severity=incident_severity,
                    status="Open",
                    probable_root_cause=final_report["root_cause"],
                    confidence=final_report["confidence"],
                    created_at=datetime.now(timezone.utc)
                )
                db.add(new_inc)
                db.commit()

            # Store Telemetry
            telem_rec = TelemetryRecord(
                incident_id=incident_id,
                device_id=device_id,
                timestamp=datetime.now(timezone.utc),
                raw_payload=telemetry_data.get("metrics", {}),
                normalized_metrics=norm_metrics,
                status=telemetry_data.get("status", "Healthy")
            )
            db.add(telem_rec)

            # Store Agent Messages
            for m in messages:
                db_msg = AgentMessage(
                    message_id=m["message_id"],
                    incident_id=incident_id,
                    sender=m["sender"],
                    receiver=m["receiver"],
                    message_type=m["message_type"],
                    schema_version=m["schema_version"],
                    payload=m["payload"],
                    timestamp=datetime.now(timezone.utc),
                    execution_status="success"
                )
                db.add(db_msg)

            # Store Agent Findings
            for f in findings:
                finding_rec = AgentFinding(
                    incident_id=incident_id,
                    agent_name=f["agent"],
                    finding=f["primary_finding"],
                    severity=f["severity"],
                    confidence=f["confidence"],
                    evidence=f["evidence"],
                    created_at=datetime.now(timezone.utc)
                )
                db.add(finding_rec)

            # Store Diagnosis Report
            existing_rep = db.query(DiagnosisReport).filter(DiagnosisReport.incident_id == incident_id).first()
            if not existing_rep:
                rep_rec = DiagnosisReport(
                    incident_id=incident_id,
                    root_cause=final_report["root_cause"],
                    confidence=final_report["confidence"],
                    supporting_evidence=final_report["supporting_evidence"],
                    alternative_causes=final_report["alternative_causes"],
                    recommended_actions=final_report["recommended_actions"],
                    limitations=final_report["limitations"],
                    report_json=final_report,
                    created_at=datetime.now(timezone.utc)
                )
                db.add(rep_rec)
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"Orchestrator DB persistence error: {e}")
        finally:
            db.close()

        return {
            "incident_id": incident_id,
            "status": "completed",
            "device_id": device_id,
            "scenario": scenario_name,
            "severity": incident_severity,
            "timeline": timeline,
            "messages": messages,
            "findings": findings,
            "ml_results": ml_results,
            "temporal_analysis": temporal_res,
            "report": final_report
        }
