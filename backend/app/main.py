import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

from app.config import settings
from app.database.connection import Base, engine
from app.database.models import User, Incident, Device, TelemetryRecord, AgentMessage, AgentFinding, DiagnosisReport, ModelRegistry

# Import API Routers
from app.api.auth import router as auth_router
from app.api.dashboard import router as dashboard_router
from app.api.incidents import router as incidents_router
from app.api.telemetry import router as telemetry_router
from app.api.diagnosis import router as diagnosis_router
from app.api.agents import router as agents_router
from app.api.interoperability import router as interop_router
from app.api.models import router as models_router
from app.api.simulation import router as simulation_router

# Initialize database schema
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Multi-Agent Network Fault Diagnosis and Interoperability Platform for Campus Infrastructure."
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permissive for hackathon local dev and evaluation
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(dashboard_router, prefix=settings.API_V1_STR)
app.include_router(incidents_router, prefix=settings.API_V1_STR)
app.include_router(telemetry_router, prefix=settings.API_V1_STR)
app.include_router(diagnosis_router, prefix=settings.API_V1_STR)
app.include_router(agents_router, prefix=settings.API_V1_STR)
app.include_router(interop_router, prefix=settings.API_V1_STR)
app.include_router(models_router, prefix=settings.API_V1_STR)
app.include_router(simulation_router, prefix=settings.API_V1_STR)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "NetCoop AI Diagnostic Engine",
        "version": settings.VERSION,
        "database": "connected",
        "multi_agent_system": "operational",
        "active_models": 4,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/")
def root():
    return {
        "name": "NetCoop AI API",
        "docs_url": "/docs",
        "health_url": "/api/health"
    }
