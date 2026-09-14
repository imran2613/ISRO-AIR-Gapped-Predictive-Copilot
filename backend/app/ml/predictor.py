from datetime import datetime, timedelta
from random import Random

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

LABELS = ["Healthy", "Warning", "Critical"]


class FailurePredictor:
    def __init__(self) -> None:
        self.encoder = LabelEncoder()
        self.model = RandomForestClassifier(n_estimators=160, max_depth=8, random_state=42)
        self._trained = False
        self.train()

    def train(self) -> None:
        rng = Random(42)
        rows: list[list[float]] = []
        labels: list[str] = []

        for _ in range(2200):
            cpu = rng.uniform(12, 99)
            memory = rng.uniform(20, 98)
            latency = rng.uniform(8, 220)
            loss = rng.uniform(0, 9)
            bandwidth = rng.uniform(15, 100)
            score = (
                cpu * 0.22
                + memory * 0.18
                + latency * 0.15
                + loss * 7.4
                + bandwidth * 0.25
            )
            if loss > 5.5 or latency > 170 or cpu > 92 or bandwidth > 96:
                label = "Critical"
            elif score > 78 or cpu > 78 or memory > 82 or bandwidth > 84 or loss > 2.5:
                label = "Warning"
            else:
                label = "Healthy"
            rows.append([cpu, memory, latency, loss, bandwidth])
            labels.append(label)

        y = self.encoder.fit_transform(labels)
        self.model.fit(np.array(rows), y)
        self._trained = True

    def predict(self, router: dict) -> dict:
        features = np.array(
            [[router["cpu"], router["memory"], router["latency"], router["packet_loss"], router["bandwidth"]]]
        )
        probabilities = self.model.predict_proba(features)[0]
        classes = self.encoder.inverse_transform(self.model.classes_)
        probability_map = {label: float(probabilities[idx]) for idx, label in enumerate(classes)}
        predicted = max(probability_map, key=probability_map.get)
        failure_probability = probability_map.get("Critical", 0.0)
        warning_probability = probability_map.get("Warning", 0.0)
        risk_score = round((failure_probability * 100) + (warning_probability * 45), 1)
        minutes = max(8, int(180 - risk_score * 1.65))
        return {
            "router_id": router["router_id"],
            "predicted_state": predicted,
            "failure_probability": round(failure_probability, 3),
            "risk_score": min(100, risk_score),
            "predicted_outage_time": (datetime.utcnow() + timedelta(minutes=minutes)).isoformat() + "Z",
        }


failure_predictor = FailurePredictor()
