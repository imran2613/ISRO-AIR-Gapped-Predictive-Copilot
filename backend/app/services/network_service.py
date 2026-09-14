from app.simulators.mpls_simulator import network_simulator


class NetworkService:
    def get_snapshot(self) -> dict:
        return network_simulator.snapshot()

    def get_routers(self) -> list[dict]:
        return self.get_snapshot()["routers"]

    def get_alerts(self, limit: int = 50) -> list[dict]:
        return self.get_snapshot()["alerts"][:limit]

    def get_metrics(self) -> dict:
        return self.get_snapshot()["metrics"]

    def get_predictions(self) -> list[dict]:
        return self.get_snapshot()["predictions"]


network_service = NetworkService()
