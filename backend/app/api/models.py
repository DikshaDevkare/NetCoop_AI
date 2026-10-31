import os
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config import settings
from app.database.connection import get_db
from app.database.models import ModelRegistry

router = APIRouter(prefix="/models", tags=["Machine Learning Models"])

@router.get("/status")
def get_models_status():
    artifacts = [
        ("Isolation Forest Anomaly Detector", "isolation_forest.joblib"),
        ("XGBoost Fault Classifier", "xgboost_fault_classifier.joblib"),
        ("Random Forest Infrastructure Classifier", "random_forest_infra.joblib"),
        ("Gradient Boosting Health Classifier", "gradient_boosting_health.joblib")
    ]

    status_list = []
    for name, filename in artifacts:
        path = os.path.join(settings.ARTIFACTS_DIR, filename)
        exists = os.path.exists(path)
        status_list.append({
            "model_name": name,
            "filename": filename,
            "status": "Loaded & Active" if exists else "Not Found",
            "ready": exists,
            "size_kb": round(os.path.getsize(path) / 1024, 1) if exists else 0
        })

    return {
        "all_ready": all(m["ready"] for m in status_list),
        "total_models": len(status_list),
        "models": status_list
    }

@router.get("/metrics")
def get_model_metrics(db: Session = Depends(get_db)):
    metrics_file = os.path.join(settings.ARTIFACTS_DIR, "evaluation_metrics.json")
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            return json.load(f)

    # Read from DB if file is missing
    records = db.query(ModelRegistry).all()
    if records:
        return {
            "source": "database_registry",
            "models": {r.model_name: r.evaluation_metrics for r in records}
        }

    return {"message": "Metrics not yet calculated. Run training pipeline."}
