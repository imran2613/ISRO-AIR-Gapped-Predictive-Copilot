import AlertTimeline from "../components/AlertTimeline";
import MetricCharts from "../components/MetricCharts";
import PredictionPanel from "../components/PredictionPanel";
import RouterTable from "../components/RouterTable";
import StatCard from "../components/StatCard";

export default function Dashboard({ live }) {
  const summary = live.metrics?.summary || {};

  if (live.loading) {
    return <div className="rounded border border-line bg-panel p-8 text-slate-300">Starting MPLS simulator...</div>;
  }

  return (
    <div className="space-y-6">
      {live.error && <div className="rounded border border-danger bg-danger/10 p-4 text-danger">{live.error}</div>}

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <StatCard label="Active Routers" value={summary.active_routers || 0} />
        <StatCard label="Healthy Routers" value={summary.healthy_routers || 0} tone="green" />
        <StatCard label="Warning Routers" value={summary.warning_routers || 0} tone="amber" />
        <StatCard label="Critical Routers" value={summary.critical_routers || 0} tone="red" />
      </div>

      <div className="grid gap-6 2xl:grid-cols-[1fr_420px]">
        <MetricCharts trends={live.metrics?.trends || []} />
        <div className="space-y-6">
          <PredictionPanel predictions={live.predictions} routers={live.routers} />
          <AlertTimeline alerts={live.alerts} />
        </div>
      </div>

      <RouterTable routers={live.routers} />
    </div>
  );
}
