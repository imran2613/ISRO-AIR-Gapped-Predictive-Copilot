from datetime import datetime, timedelta
from random import Random
from uuid import uuid4

from app.database.sqlite import get_connection, init_db
from app.ml.predictor import failure_predictor
from app.services.anomaly_service import detect_anomalies
from app.services.recommendation_service import recommendations_for, root_cause


class MPLSNetworkSimulator:
    def __init__(self) -> None:
        self.rng = Random(7)
        self.routers: list[dict] = []
        self.metric_history: list[dict] = []
        self.alerts: list[dict] = []
        self.incidents: list[dict] = []
        self.tick = 0
        self.is_custom_mode = False

    def bootstrap(self) -> None:
        if self.routers:
            return
        init_db()
        sites = ["SDSC-SHAR", "ISTRAC-BLR", "VSSC-TVM", "URSC-BLR", "NRSC-HYD", "MCF-HSN", "LPSC-MDL", "SAC-AMD"]
        for idx, site in enumerate(sites, start=1):
            self.routers.append(
                {
                    "router_id": f"R{idx}",
                    "site": site,
                    "cpu": self.rng.uniform(18, 55),
                    "memory": self.rng.uniform(32, 68),
                    "link_status": "up",
                    "latency": self.rng.uniform(18, 55),
                    "packet_loss": self.rng.uniform(0.02, 0.7),
                    "bandwidth": self.rng.uniform(28, 72),
                    "traffic_volume": self.rng.uniform(1.8, 7.5),
                    "status": "Healthy",
                    "severity": "low",
                    "last_updated": datetime.utcnow().isoformat() + "Z",
                    "root_cause": "No abnormal pattern detected.",
                    "recommendations": ["Continue monitoring. No corrective action is required for this router right now."],
                }
            )
        for _ in range(16):
            self.update()

    def update(self) -> None:
        if not self.routers:
            self.bootstrap()
            return
        
        now = datetime.utcnow()
        if self.is_custom_mode:
            # Keep custom telemetry values constant, only update timestamp.
            for router in self.routers:
                router["last_updated"] = now.isoformat() + "Z"
            return

        self.tick += 1
        hot_router = self.tick % len(self.routers)
        for idx, router in enumerate(self.routers):
            drift = 1.0 if idx != hot_router else 2.8
            router["cpu"] = self._bounded(router["cpu"] + self.rng.uniform(-5, 7) * drift, 8, 99)
            router["memory"] = self._bounded(router["memory"] + self.rng.uniform(-2, 3.8) * drift, 18, 98)
            router["latency"] = self._bounded(router["latency"] + self.rng.uniform(-8, 13) * drift, 8, 230)
            router["packet_loss"] = self._bounded(router["packet_loss"] + self.rng.uniform(-0.25, 0.55) * drift, 0, 9)
            router["bandwidth"] = self._bounded(router["bandwidth"] + self.rng.uniform(-7, 9) * drift, 5, 100)
            router["traffic_volume"] = self._bounded(router["bandwidth"] / 11 + self.rng.uniform(-0.8, 1.4), 0.4, 12.5)
            router["link_status"] = "down" if self.rng.random() < 0.015 and idx == hot_router else "up"
            router["last_updated"] = now.isoformat() + "Z"

            anomalies = detect_anomalies(router)
            prediction = failure_predictor.predict(router)
            router["prediction"] = prediction
            router["status"] = prediction["predicted_state"]
            router["severity"] = "critical" if router["status"] == "Critical" else "warning" if router["status"] == "Warning" else "low"
            router["root_cause"] = root_cause(router, anomalies)
            router["recommendations"] = recommendations_for(router, anomalies)
            self._record_alerts(router, anomalies, now)

        self.metric_history.append(
            {
                "time": now.strftime("%H:%M:%S"),
                "cpu": round(sum(r["cpu"] for r in self.routers) / len(self.routers), 1),
                "latency": round(sum(r["latency"] for r in self.routers) / len(self.routers), 1),
                "packet_loss": round(sum(r["packet_loss"] for r in self.routers) / len(self.routers), 2),
                "traffic": round(sum(r["traffic_volume"] for r in self.routers), 2),
                "bandwidth": round(sum(r["bandwidth"] for r in self.routers) / len(self.routers), 1),
            }
        )
        self.metric_history = self.metric_history[-40:]
        self.alerts = self.alerts[-120:]
        self.incidents = self.incidents[-80:]

    def snapshot(self) -> dict:
        if not self.routers:
            self.bootstrap()
        self.update()
        predictions = [router["prediction"] for router in self.routers]
        return {
            "routers": self.routers,
            "alerts": list(reversed(self.alerts)),
            "metrics": {
                "is_custom_mode": self.is_custom_mode,
                "summary": self.summary(),
                "trends": self.metric_history,
                "generated_at": datetime.utcnow().isoformat() + "Z",
            },
            "predictions": sorted(predictions, key=lambda item: item["risk_score"], reverse=True),
            "incidents": list(reversed(self.incidents)),
        }

    def summary(self) -> dict:
        return {
            "active_routers": len(self.routers),
            "healthy_routers": sum(1 for r in self.routers if r["status"] == "Healthy"),
            "warning_routers": sum(1 for r in self.routers if r["status"] == "Warning"),
            "critical_routers": sum(1 for r in self.routers if r["status"] == "Critical"),
        }

    def _record_alerts(self, router: dict, anomalies: list[dict], now: datetime) -> None:
        for anomaly in anomalies:
            if self.alerts and self.alerts[-1]["router_id"] == router["router_id"] and self.alerts[-1]["category"] == anomaly["category"]:
                continue
            alert = {
                "id": str(uuid4()),
                "router_id": router["router_id"],
                "severity": anomaly["severity"],
                "category": anomaly["category"],
                "message": anomaly["message"],
                "created_at": now.isoformat() + "Z",
                "status": "open",
            }
            self.alerts.append(alert)
            if anomaly["severity"] == "critical":
                incident = {
                    "id": str(uuid4()),
                    "router_id": router["router_id"],
                    "title": anomaly["category"],
                    "severity": anomaly["severity"],
                    "description": router["root_cause"],
                    "created_at": (now + timedelta(seconds=2)).isoformat() + "Z",
                    "resolution": "Pending NOC action",
                }
                self.incidents.append(incident)
                self._persist(alert, incident)

    def _persist(self, alert: dict, incident: dict) -> None:
        conn = get_connection()
        try:
            conn.execute(
                "INSERT OR IGNORE INTO alerts VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    alert["id"],
                    alert["router_id"],
                    alert["severity"],
                    alert["category"],
                    alert["message"],
                    alert["created_at"],
                    alert["status"],
                ),
            )
            conn.execute(
                "INSERT OR IGNORE INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    incident["id"],
                    incident["router_id"],
                    incident["title"],
                    incident["severity"],
                    incident["description"],
                    incident["created_at"],
                    incident["resolution"],
                ),
            )
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def _bounded(value: float, low: float, high: float) -> float:
        return round(max(low, min(high, value)), 2)

    def import_custom_data(self, data: list[dict]) -> None:
        self.is_custom_mode = True
        self.routers = []
        now = datetime.utcnow()
        for idx, row in enumerate(data):
            router_id = row.get("router_id", f"Custom-R{idx+1}")
            router = {
                "router_id": router_id,
                "site": row.get("site", f"Custom Site {idx+1}"),
                "cpu": float(row.get("cpu", 0)),
                "memory": float(row.get("memory", 0)),
                "latency": float(row.get("latency", 0)),
                "packet_loss": float(row.get("packet_loss", 0)),
                "bandwidth": float(row.get("bandwidth", 0)),
                "traffic_volume": float(row.get("traffic_volume", row.get("bandwidth", 0) / 11)),
                "link_status": row.get("link_status", "up"),
                "last_updated": now.isoformat() + "Z",
            }
            anomalies = detect_anomalies(router)
            prediction = failure_predictor.predict(router)
            router["prediction"] = prediction
            router["status"] = prediction["predicted_state"]
            router["severity"] = "critical" if router["status"] == "Critical" else "warning" if router["status"] == "Warning" else "low"
            router["root_cause"] = root_cause(router, anomalies)
            router["recommendations"] = recommendations_for(router, anomalies)
            self.routers.append(router)
            self._record_alerts(router, anomalies, now)

    def reset_simulation(self) -> None:
        self.is_custom_mode = False
        self.routers = []
        self.tick = 0
        self.bootstrap()


network_simulator = MPLSNetworkSimulator()
