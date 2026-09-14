const severityColor = {
  critical: "border-danger text-danger",
  warning: "border-amber text-amber",
  low: "border-cyan text-cyan"
};

export default function AlertTimeline({ alerts = [] }) {
  return (
    <section className="rounded border border-line bg-panel p-4">
      <h3 className="font-semibold">Incident Timeline</h3>
      <div className="mt-4 max-h-[440px] space-y-3 overflow-y-auto pr-1">
        {alerts.slice(0, 14).map((alert) => (
          <div key={alert.id} className={`border-l-2 pl-3 ${severityColor[alert.severity] || severityColor.low}`}>
            <div className="flex flex-wrap items-center justify-between gap-2">
              <p className="text-sm font-semibold">{alert.category}</p>
              <span className="text-xs text-slate-400">{new Date(alert.created_at).toLocaleTimeString()}</span>
            </div>
            <p className="mt-1 text-sm text-slate-300">{alert.message}</p>
            <p className="mt-1 text-xs uppercase tracking-wider">{alert.router_id} · {alert.severity}</p>
          </div>
        ))}
        {!alerts.length && <p className="text-sm text-slate-400">No active alerts in the current telemetry window.</p>}
      </div>
    </section>
  );
}
