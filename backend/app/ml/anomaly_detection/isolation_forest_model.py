import os
import joblib
import numpy as np
from typing import Dict, Any, List, Optional
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

ANOMALY_FEATURES = [
    "latency_ms",
    "packet_loss_pct",
    "jitter_ms",
    "cpu_usage_pct",
    "memory_usage_pct",
    "link_utilization_pct",
    "queue_drops",
    "interface_errors"
]

class IsolationForestAnomalyDetector:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model: Optional[IsolationForest] = None
        self.scaler: Optional[StandardScaler] = None
        self.threshold: float = 0.0
        self.metadata: Dict[str, Any] = {
            "model_name": "Isolation Forest Anomaly Detector",
            "model_type": "IsolationForest",
            "version": "1.0.0",
            "features": ANOMALY_FEATURES
        }

    def train(self, X: np.ndarray, contamination: float = 0.08, random_state: int = 42):
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = IsolationForest(
            n_estimators=150,
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )
        self.model.fit(X_scaled)
        
        # Decision function: lower values indicate abnormal points
        scores = self.model.decision_function(X_scaled)
        self.threshold = float(np.percentile(scores, contamination * 100))
        self.metadata["threshold"] = self.threshold
        self.metadata["contamination"] = contamination

    def predict(self, feature_dict: Dict[str, Any]) -> Dict[str, Any]:
        if self.model is None or self.scaler is None:
            raise RuntimeError("Isolation Forest model is not trained or loaded.")

        vector = [float(feature_dict.get(feat, 0.0) or 0.0) for feat in ANOMALY_FEATURES]
        X_vec = np.array([vector])
        X_scaled = self.scaler.transform(X_vec)

        raw_pred = int(self.model.predict(X_scaled)[0]) # -1 = anomaly, 1 = normal
        raw_score = float(self.model.decision_function(X_scaled)[0])
        
        # Normalize score into [0.0, 1.0] where 1.0 = highly anomalous
        # decision_function is centered roughly around 0; negative is anomaly
        anomaly_prob = float(1.0 / (1.0 + np.exp(raw_score * 5.0)))
        is_anomaly = bool(raw_pred == -1 or raw_score < self.threshold)

        return {
            "is_anomaly": is_anomaly,
            "anomaly_score": round(anomaly_prob, 4),
            "decision_score": round(raw_score, 4),
            "threshold": round(self.threshold, 4),
            "evaluated_features": {feat: vector[i] for i, feat in enumerate(ANOMALY_FEATURES)},
            "model": self.metadata["model_name"]
        }

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            "model": self.model,
            "scaler": self.scaler,
            "threshold": self.threshold,
            "metadata": self.metadata
        }, filepath)

    def load(self, filepath: str):
        data = joblib.load(filepath)
        self.model = data["model"]
        self.scaler = data["scaler"]
        self.threshold = data["threshold"]
        self.metadata = data["metadata"]
