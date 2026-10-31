import os
import joblib
import numpy as np
from typing import Dict, Any, List, Optional
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler

INFRA_FEATURES = [
    "cpu_usage_pct",
    "memory_usage_pct",
    "link_utilization_pct",
    "queue_drops",
    "interface_errors",
    "latency_ms",
    "packet_loss_pct"
]

class RandomForestInfraClassifier:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path
        self.model: Optional[RandomForestClassifier] = None
        self.scaler: Optional[StandardScaler] = None
        self.encoder: Optional[LabelEncoder] = None
        self.metadata: Dict[str, Any] = {
            "model_name": "Random Forest Infrastructure Classifier",
            "model_type": "RandomForestClassifier",
            "version": "1.0.0",
            "features": INFRA_FEATURES
        }

    def train(self, X: np.ndarray, y: np.ndarray, random_state: int = 42):
        self.encoder = LabelEncoder()
        y_encoded = self.encoder.fit_transform(y)

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        self.model = RandomForestClassifier(
            n_estimators=180,
            max_depth=6,
            random_state=random_state,
            n_jobs=-1
        )
        self.model.fit(X_scaled, y_encoded)
        self.metadata["classes"] = list(self.encoder.classes_)

        importances = self.model.feature_importances_
        self.metadata["feature_importance"] = {
            feat: round(float(importances[i]), 4) for i, feat in enumerate(INFRA_FEATURES)
        }

    def predict(self, feature_dict: Dict[str, Any]) -> Dict[str, Any]:
        if self.model is None or self.scaler is None or self.encoder is None:
            raise RuntimeError("Random Forest Infrastructure Classifier is not trained or loaded.")

        vector = [float(feature_dict.get(feat, 0.0) or 0.0) for feat in INFRA_FEATURES]
        X_vec = np.array([vector])
        X_scaled = self.scaler.transform(X_vec)

        pred_idx = int(self.model.predict(X_scaled)[0])
        probabilities = self.model.predict_proba(X_scaled)[0]

        predicted_class = self.encoder.classes_[pred_idx]
        class_probs = {
            self.encoder.classes_[i]: round(float(prob), 4)
            for i, prob in enumerate(probabilities)
        }

        return {
            "predicted_condition": predicted_class,
            "confidence": round(float(probabilities[pred_idx]), 4),
            "probabilities": class_probs,
            "feature_importance": self.metadata.get("feature_importance", {}),
            "model": self.metadata["model_name"]
        }

    def save(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump({
            "model": self.model,
            "scaler": self.scaler,
            "encoder": self.encoder,
            "metadata": self.metadata
        }, filepath)

    def load(self, filepath: str):
        data = joblib.load(filepath)
        self.model = data["model"]
        self.scaler = data["scaler"]
        self.encoder = data["encoder"]
        self.metadata = data["metadata"]
