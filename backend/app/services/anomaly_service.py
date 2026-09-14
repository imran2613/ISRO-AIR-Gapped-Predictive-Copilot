def detect_anomalies(router: dict) -> list[dict]:
    anomalies: list[dict] = []
    checks = [
        ("High CPU", router["cpu"] > 85, "critical" if router["cpu"] > 93 else "warning"),
        ("Memory Leak", router["memory"] > 84, "critical" if router["memory"] > 93 else "warning"),
        ("Latency Spike", router["latency"] > 120, "critical" if router["latency"] > 175 else "warning"),
        ("Packet Loss Surge", router["packet_loss"] > 2.0, "critical" if router["packet_loss"] > 5 else "warning"),
        ("Link Failure", router["link_status"] == "down", "critical"),
        ("Traffic Congestion", router["bandwidth"] > 88, "critical" if router["bandwidth"] > 96 else "warning"),
    ]
    for category, triggered, severity in checks:
        if triggered:
            anomalies.append(
                {
                    "router_id": router["router_id"],
                    "category": category,
                    "severity": severity,
                    "message": build_message(category, router),
                }
            )
    return anomalies


def build_message(category: str, router: dict) -> str:
    if category == "High CPU":
        return f"{router['router_id']} CPU utilization is elevated at {router['cpu']:.1f}%."
    if category == "Memory Leak":
        return f"{router['router_id']} memory usage is trending high at {router['memory']:.1f}%."
    if category == "Latency Spike":
        return f"{router['router_id']} latency increased to {router['latency']:.1f} ms."
    if category == "Packet Loss Surge":
        return f"{router['router_id']} packet loss reached {router['packet_loss']:.2f}%."
    if category == "Link Failure":
        return f"{router['router_id']} MPLS link is down and traffic may require reroute."
    return f"{router['router_id']} bandwidth utilization is {router['bandwidth']:.1f}%."
