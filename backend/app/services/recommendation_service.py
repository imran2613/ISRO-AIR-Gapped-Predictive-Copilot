def recommendations_for(router: dict, anomalies: list[dict]) -> list[str]:
    categories = {item["category"] for item in anomalies}
    actions: list[str] = []
    if "Link Failure" in categories:
        actions.append("Re-route MPLS traffic through the secondary LSP and verify label distribution.")
        actions.append("Investigate optical interface, transceiver health, and provider handoff.")
    if "Traffic Congestion" in categories:
        actions.append("Shift non-critical traffic to an alternate path and review QoS queues.")
        actions.append("Plan capacity upgrade if utilization remains above 85% for the next hour.")
    if "Packet Loss Surge" in categories:
        actions.append("Check interface errors, MTU mismatch, and congestion drops on adjacent routers.")
    if "Latency Spike" in categories:
        actions.append("Validate path changes, jitter, and underlay transport delay before rerouting.")
    if "High CPU" in categories:
        actions.append("Restart non-essential routing services during a maintenance-safe window.")
    if "Memory Leak" in categories:
        actions.append("Capture process memory snapshot and prepare controlled router reload if growth persists.")
    if not actions:
        actions.append("Continue monitoring. No corrective action is required for this router right now.")
    return actions


def root_cause(router: dict, anomalies: list[dict]) -> str:
    categories = {item["category"] for item in anomalies}
    if {"Traffic Congestion", "Packet Loss Surge"} <= categories:
        return (
            f"Router {router['router_id']} is likely experiencing congestion due to sustained bandwidth "
            f"utilization at {router['bandwidth']:.1f}% combined with packet loss of {router['packet_loss']:.2f}%."
        )
    if {"High CPU", "Latency Spike"} <= categories:
        return (
            f"Router {router['router_id']} appears compute-bound: CPU is {router['cpu']:.1f}% while "
            f"latency has climbed to {router['latency']:.1f} ms."
        )
    if "Link Failure" in categories:
        return f"Router {router['router_id']} has a down MPLS link, indicating transport or interface failure."
    if "Memory Leak" in categories:
        return f"Router {router['router_id']} shows high memory pressure and may have a leaking routing process."
    if anomalies:
        return anomalies[0]["message"]
    return f"Router {router['router_id']} is operating within expected MPLS telemetry thresholds."
