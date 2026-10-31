import os
import json
import numpy as np
from datetime import datetime, timezone
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

from app.ml.datasets.generator import generate_synthetic_dataset
from app.ml.anomaly_detection.isolation_forest_model import IsolationForestAnomalyDetector, ANOMALY_FEATURES
from app.ml.fault_classification.xgboost_model import XGBoostFaultClassifier, XGB_FEATURES
from app.ml.infrastructure_classification.random_forest_model import RandomForestInfraClassifier, INFRA_FEATURES
from app.ml.network_health_classification.gradient_boosting_model import GradientBoostingHealthClassifier, HEALTH_FEATURES

from app.database.connection import SessionLocal, Base, engine
from app.database.models import ModelRegistry

def run_training_pipeline(output_dir: str = None) -> dict:
    if output_dir is None:
        output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "artifacts"))
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("NetCoop AI: Training Four Machine Learning Models")
    print("=" * 60)

    # 1. Dataset Generation
    print("Generating reproducible synthetic dataset (70% train, 15% val, 15% test by incident)...")
    train_df, val_df, test_df = generate_synthetic_dataset(num_incidents=400, records_per_incident=12, base_seed=42)
    print(f"Dataset split: Train={len(train_df)} rows, Val={len(val_df)} rows, Test={len(test_df)} rows.")

    metrics_summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "dataset": {
            "type": "reproducible_synthetic_simulation",
            "train_samples": len(train_df),
            "val_samples": len(val_df),
            "test_samples": len(test_df),
            "train_incidents": int(train_df["incident_id"].nunique()),
            "val_incidents": int(val_df["incident_id"].nunique()),
            "test_incidents": int(test_df["incident_id"].nunique()),
        },
        "models": {}
    }

    # -------------------------------------------------------------
    # MODEL 1: Isolation Forest (Anomaly Detection)
    # -------------------------------------------------------------
    print("\n--- Training Model 1: Isolation Forest ---")
    iso_model = IsolationForestAnomalyDetector()
    X_iso_train = train_df[train_df["is_anomaly"] == 0][ANOMALY_FEATURES].values # Train primarily on normal
    # Supplement with small contamination
    X_iso_all = train_df[ANOMALY_FEATURES].values
    iso_model.train(X_iso_all, contamination=0.10, random_state=42)

    # Evaluate on test set
    X_iso_test = test_df[ANOMALY_FEATURES].values
    y_iso_test = test_df["is_anomaly"].values
    
    # Predict on test
    iso_preds = []
    for row_vals in X_iso_test:
        fdict = {ANOMALY_FEATURES[i]: row_vals[i] for i in range(len(ANOMALY_FEATURES))}
        res = iso_model.predict(fdict)
        iso_preds.append(1 if res["is_anomaly"] else 0)

    iso_acc = accuracy_score(y_iso_test, iso_preds)
    iso_prec = precision_score(y_iso_test, iso_preds, zero_division=0)
    iso_rec = recall_score(y_iso_test, iso_preds, zero_division=0)
    iso_f1 = f1_score(y_iso_test, iso_preds, zero_division=0)
    iso_cm = confusion_matrix(y_iso_test, iso_preds).tolist()

    iso_path = os.path.join(output_dir, "isolation_forest.joblib")
    iso_model.save(iso_path)
    print(f"Model 1 Saved -> {iso_path}")
    print(f"Isolation Forest Test F1: {iso_f1:.4f}, Accuracy: {iso_acc:.4f}, Recall: {iso_rec:.4f}")

    metrics_summary["models"]["isolation_forest"] = {
        "model_name": "Isolation Forest Anomaly Detector",
        "accuracy": round(float(iso_acc), 4),
        "precision": round(float(iso_prec), 4),
        "recall": round(float(iso_rec), 4),
        "f1_score": round(float(iso_f1), 4),
        "confusion_matrix": iso_cm,
        "artifact_path": iso_path,
        "features": ANOMALY_FEATURES
    }

    # -------------------------------------------------------------
    # MODEL 2: XGBoost Classifier (Network Fault Classification)
    # -------------------------------------------------------------
    print("\n--- Training Model 2: XGBoost Classifier ---")
    xgb_model = XGBoostFaultClassifier()
    X_xgb_train = train_df[XGB_FEATURES].values
    y_xgb_train = train_df["scenario"].values
    xgb_model.train(X_xgb_train, y_xgb_train, random_state=42)

    X_xgb_test = test_df[XGB_FEATURES].values
    y_xgb_test = test_df["scenario"].values

    xgb_preds = []
    for row_vals in X_xgb_test:
        fdict = {XGB_FEATURES[i]: row_vals[i] for i in range(len(XGB_FEATURES))}
        res = xgb_model.predict(fdict)
        xgb_preds.append(res["predicted_fault"])

    xgb_acc = accuracy_score(y_xgb_test, xgb_preds)
    xgb_prec = precision_score(y_xgb_test, xgb_preds, average="weighted", zero_division=0)
    xgb_rec = recall_score(y_xgb_test, xgb_preds, average="weighted", zero_division=0)
    xgb_f1 = f1_score(y_xgb_test, xgb_preds, average="weighted", zero_division=0)
    xgb_cm = confusion_matrix(y_xgb_test, xgb_preds).tolist()
    xgb_report = classification_report(y_xgb_test, xgb_preds, output_dict=True, zero_division=0)

    xgb_path = os.path.join(output_dir, "xgboost_fault_classifier.joblib")
    xgb_model.save(xgb_path)
    print(f"Model 2 Saved -> {xgb_path}")
    print(f"XGBoost Test Accuracy: {xgb_acc:.4f}, F1 (weighted): {xgb_f1:.4f}")

    metrics_summary["models"]["xgboost_fault_classifier"] = {
        "model_name": "XGBoost Fault Classifier",
        "accuracy": round(float(xgb_acc), 4),
        "precision": round(float(xgb_prec), 4),
        "recall": round(float(xgb_rec), 4),
        "f1_score": round(float(xgb_f1), 4),
        "confusion_matrix": xgb_cm,
        "classification_report": xgb_report,
        "feature_importance": xgb_model.metadata.get("feature_importance", {}),
        "artifact_path": xgb_path,
        "features": XGB_FEATURES
    }

    # -------------------------------------------------------------
    # MODEL 3: Random Forest Classifier (Infrastructure Condition)
    # -------------------------------------------------------------
    print("\n--- Training Model 3: Random Forest Classifier ---")
    rf_model = RandomForestInfraClassifier()
    X_rf_train = train_df[INFRA_FEATURES].values
    y_rf_train = train_df["infra_condition"].values
    rf_model.train(X_rf_train, y_rf_train, random_state=42)

    X_rf_test = test_df[INFRA_FEATURES].values
    y_rf_test = test_df["infra_condition"].values

    rf_preds = []
    for row_vals in X_rf_test:
        fdict = {INFRA_FEATURES[i]: row_vals[i] for i in range(len(INFRA_FEATURES))}
        res = rf_model.predict(fdict)
        rf_preds.append(res["predicted_condition"])

    rf_acc = accuracy_score(y_rf_test, rf_preds)
    rf_prec = precision_score(y_rf_test, rf_preds, average="weighted", zero_division=0)
    rf_rec = recall_score(y_rf_test, rf_preds, average="weighted", zero_division=0)
    rf_f1 = f1_score(y_rf_test, rf_preds, average="weighted", zero_division=0)
    rf_cm = confusion_matrix(y_rf_test, rf_preds).tolist()

    rf_path = os.path.join(output_dir, "random_forest_infra.joblib")
    rf_model.save(rf_path)
    print(f"Model 3 Saved -> {rf_path}")
    print(f"Random Forest Test Accuracy: {rf_acc:.4f}, F1 (weighted): {rf_f1:.4f}")

    metrics_summary["models"]["random_forest_infra"] = {
        "model_name": "Random Forest Infrastructure Classifier",
        "accuracy": round(float(rf_acc), 4),
        "precision": round(float(rf_prec), 4),
        "recall": round(float(rf_rec), 4),
        "f1_score": round(float(rf_f1), 4),
        "confusion_matrix": rf_cm,
        "feature_importance": rf_model.metadata.get("feature_importance", {}),
        "artifact_path": rf_path,
        "features": INFRA_FEATURES
    }

    # -------------------------------------------------------------
    # MODEL 4: Gradient Boosting (Network Health State)
    # -------------------------------------------------------------
    print("\n--- Training Model 4: Gradient Boosting Classifier ---")
    gb_model = GradientBoostingHealthClassifier()
    X_gb_train = train_df[HEALTH_FEATURES].values
    y_gb_train = train_df["health_state"].values
    gb_model.train(X_gb_train, y_gb_train, random_state=42)

    X_gb_test = test_df[HEALTH_FEATURES].values
    y_gb_test = test_df["health_state"].values

    gb_preds = []
    for row_vals in X_gb_test:
        fdict = {HEALTH_FEATURES[i]: row_vals[i] for i in range(len(HEALTH_FEATURES))}
        res = gb_model.predict(fdict)
        gb_preds.append(res["predicted_health"])

    gb_acc = accuracy_score(y_gb_test, gb_preds)
    gb_prec = precision_score(y_gb_test, gb_preds, average="weighted", zero_division=0)
    gb_rec = recall_score(y_gb_test, gb_preds, average="weighted", zero_division=0)
    gb_f1 = f1_score(y_gb_test, gb_preds, average="weighted", zero_division=0)
    gb_cm = confusion_matrix(y_gb_test, gb_preds).tolist()

    gb_path = os.path.join(output_dir, "gradient_boosting_health.joblib")
    gb_model.save(gb_path)
    print(f"Model 4 Saved -> {gb_path}")
    print(f"Gradient Boosting Test Accuracy: {gb_acc:.4f}, F1 (weighted): {gb_f1:.4f}")

    metrics_summary["models"]["gradient_boosting_health"] = {
        "model_name": "Gradient Boosting Health Classifier",
        "accuracy": round(float(gb_acc), 4),
        "precision": round(float(gb_prec), 4),
        "recall": round(float(gb_rec), 4),
        "f1_score": round(float(gb_f1), 4),
        "confusion_matrix": gb_cm,
        "feature_importance": gb_model.metadata.get("feature_importance", {}),
        "artifact_path": gb_path,
        "features": HEALTH_FEATURES
    }

    # Write metrics JSON
    metrics_json_path = os.path.join(output_dir, "evaluation_metrics.json")
    with open(metrics_json_path, "w") as f:
        json.dump(metrics_summary, f, indent=2)
    print(f"\nAll metrics successfully written to: {metrics_json_path}")

    # Register in Database
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        db.query(ModelRegistry).delete()
        for key, mdata in metrics_summary["models"].items():
            reg = ModelRegistry(
                model_name=mdata["model_name"],
                model_version="1.0.0",
                model_path=mdata["artifact_path"],
                training_timestamp=datetime.now(timezone.utc),
                evaluation_metrics=mdata,
                status="Active"
            )
            db.add(reg)
        db.commit()
        print("Database Model Registry updated with all 4 trained models.")
    except Exception as e:
        db.rollback()
        print(f"Warning: Database registry update had issue: {e}")
    finally:
        db.close()

    return metrics_summary

if __name__ == "__main__":
    run_training_pipeline()
