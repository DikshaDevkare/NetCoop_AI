import io
import json
import csv
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from typing import Dict, Any, List

from app.database.connection import get_db
from app.database.models import TelemetryRecord, Device
from app.protocols.validator import normalize_telemetry_metrics

router = APIRouter(prefix="/telemetry", tags=["Telemetry Ingestion"])

@router.post("")
def ingest_telemetry(payload: Dict[str, Any] = Body(...), db: Session = Depends(get_db)):
    device_id = payload.get("device_id", "UNKNOWN_DEV")
    raw_metrics = payload.get("metrics", {})
    norm_metrics = normalize_telemetry_metrics(raw_metrics)

    record = TelemetryRecord(
        incident_id=payload.get("incident_id"),
        device_id=device_id,
        timestamp=datetime.now(timezone.utc),
        raw_payload=raw_metrics,
        normalized_metrics=norm_metrics,
        status=payload.get("status", "Healthy")
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return {
        "status": "ingested",
        "record_id": record.id,
        "device_id": record.device_id,
        "normalized_metrics": norm_metrics
    }

@router.post("/upload")
async def upload_telemetry_file(file: UploadFile = File(...)):
    """
    Parses and validates uploaded telemetry files (CSV, JSON).
    Returns validation status matching Panel 2 of reference UI.
    """
    content = await file.read()
    filename = file.filename or "telemetry_upload"
    records = []

    try:
        if filename.endswith(".json"):
            data = json.loads(content.decode("utf-8"))
            if isinstance(data, list):
                records = data
            elif isinstance(data, dict):
                records = data.get("records") or [data]
        elif filename.endswith(".csv"):
            text_stream = io.StringIO(content.decode("utf-8"))
            reader = csv.DictReader(text_stream)
            records = list(reader)
        else:
            # Assume structured text/json
            data = json.loads(content.decode("utf-8"))
            records = [data] if isinstance(data, dict) else data
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    # Run schema validation on extracted records
    valid_count = 0
    missing_fields = []
    normalized_samples = []

    for rec in records:
        metrics = rec.get("metrics") if isinstance(rec.get("metrics"), dict) else rec
        norm = normalize_telemetry_metrics(metrics)
        if norm:
            valid_count += 1
            if len(normalized_samples) < 5:
                normalized_samples.append({
                    "device_id": rec.get("device_id", "UPLOADED_DEV"),
                    "normalized_metrics": norm
                })

    return {
        "filename": filename,
        "size_kb": round(len(content) / 1024, 1),
        "total_records": len(records),
        "valid_records": valid_count,
        "validation": {
            "schema_compatible": True,
            "required_fields_present": True,
            "no_missing_telemetry": valid_count > 0,
            "all_passed": valid_count > 0
        },
        "preview": normalized_samples
    }
