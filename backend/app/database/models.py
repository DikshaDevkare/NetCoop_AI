from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    organization = Column(String(150), default="Campus IT")
    role = Column(String(50), default="Network Administrator")
    created_at = Column(DateTime, default=datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(60), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    severity = Column(String(30), default="Medium") # Low, Medium, High, Critical
    status = Column(String(30), default="Open") # Open, In Progress, Resolved
    probable_root_cause = Column(String(250), nullable=True)
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    telemetries = relationship("TelemetryRecord", back_populates="incident", cascade="all, delete-orphan")
    messages = relationship("AgentMessage", back_populates="incident", cascade="all, delete-orphan")
    findings = relationship("AgentFinding", back_populates="incident", cascade="all, delete-orphan")
    report = relationship("DiagnosisReport", uselist=False, back_populates="incident", cascade="all, delete-orphan")

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(String(60), unique=True, index=True, nullable=False)
    device_type = Column(String(60), nullable=False) # Core Switch, Branch Router, Access Point, Server
    hostname = Column(String(120), nullable=False)
    network_segment = Column(String(80), nullable=False) # Core, Building A, Building B, Hostel, Lecture Hall
    status = Column(String(30), default="Healthy") # Healthy, Warning, Degraded, Critical

class TelemetryRecord(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(60), ForeignKey("incidents.incident_id"), nullable=True)
    device_id = Column(String(60), index=True, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    raw_payload = Column(JSON, nullable=False)
    normalized_metrics = Column(JSON, nullable=False)
    status = Column(String(30), default="Healthy")

    incident = relationship("Incident", back_populates="telemetries")

class AgentMessage(Base):
    __tablename__ = "agent_messages"

    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(60), unique=True, index=True, nullable=False)
    incident_id = Column(String(60), ForeignKey("incidents.incident_id"), nullable=True)
    sender = Column(String(80), nullable=False)
    receiver = Column(String(80), nullable=False)
    message_type = Column(String(80), nullable=False)
    schema_version = Column(String(20), default="1.0")
    payload = Column(JSON, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    execution_status = Column(String(30), default="success")

    incident = relationship("Incident", back_populates="messages")

class AgentFinding(Base):
    __tablename__ = "agent_findings"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(60), ForeignKey("incidents.incident_id"), nullable=False)
    agent_name = Column(String(80), nullable=False)
    finding = Column(String(200), nullable=False)
    severity = Column(String(30), default="medium")
    confidence = Column(Float, default=0.0)
    evidence = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="findings")

class DiagnosisReport(Base):
    __tablename__ = "diagnosis_reports"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String(60), ForeignKey("incidents.incident_id"), unique=True, nullable=False)
    root_cause = Column(String(250), nullable=False)
    confidence = Column(Float, nullable=False)
    supporting_evidence = Column(JSON, nullable=False)
    alternative_causes = Column(JSON, nullable=False)
    recommended_actions = Column(JSON, nullable=False)
    limitations = Column(JSON, nullable=False)
    report_json = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    incident = relationship("Incident", back_populates="report")

class ModelRegistry(Base):
    __tablename__ = "model_registry"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(100), nullable=False)
    model_version = Column(String(30), nullable=False)
    model_path = Column(String(255), nullable=False)
    training_timestamp = Column(DateTime, default=datetime.utcnow)
    evaluation_metrics = Column(JSON, nullable=False)
    status = Column(String(30), default="Active")
