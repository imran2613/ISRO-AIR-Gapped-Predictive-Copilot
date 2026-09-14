from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RouterState:
    router_id: str
    site: str
    cpu: float
    memory: float
    link_status: str
    latency: float
    packet_loss: float
    bandwidth: float
    traffic_volume: float
    status: str = "Healthy"
    severity: str = "low"
    last_updated: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Alert:
    id: str
    router_id: str
    severity: str
    category: str
    message: str
    created_at: str
    status: str = "open"
