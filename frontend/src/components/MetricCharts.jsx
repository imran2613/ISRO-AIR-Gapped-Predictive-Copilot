import { Area, AreaChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

function Panel({ title, children }) {
  return (
    <section className="rounded border border-line bg-panel p-4">
      <h3 className="mb-3 text-sm font-semibold text-slate-200">{title}</h3>
      <div className="h-56">{children}</div>
    </section>
  );
}

export default function MetricCharts({ trends = [] }) {
  return (
    <div className="grid gap-4 xl:grid-cols-2">
      <Panel title="CPU Trends">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={trends}>
            <CartesianGrid stroke="#263244" />
            <XAxis dataKey="time" stroke="#94a3b8" tick={{ fontSize: 11 }} />
            <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
            <Tooltip contentStyle={{ background: "#101827", border: "1px solid #263244" }} />
            <Area type="monotone" dataKey="cpu" stroke="#22d3ee" fill="#22d3ee33" />
          </AreaChart>
        </ResponsiveContainer>
      </Panel>
      <Panel title="Latency Trends">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={trends}>
            <CartesianGrid stroke="#263244" />
            <XAxis dataKey="time" stroke="#94a3b8" tick={{ fontSize: 11 }} />
            <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
            <Tooltip contentStyle={{ background: "#101827", border: "1px solid #263244" }} />
            <Line type="monotone" dataKey="latency" stroke="#f59e0b" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </Panel>
      <Panel title="Packet Loss Trends">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={trends}>
            <CartesianGrid stroke="#263244" />
            <XAxis dataKey="time" stroke="#94a3b8" tick={{ fontSize: 11 }} />
            <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
            <Tooltip contentStyle={{ background: "#101827", border: "1px solid #263244" }} />
            <Line type="monotone" dataKey="packet_loss" stroke="#ef4444" strokeWidth={2} dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </Panel>
      <Panel title="Traffic Utilization">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={trends}>
            <CartesianGrid stroke="#263244" />
            <XAxis dataKey="time" stroke="#94a3b8" tick={{ fontSize: 11 }} />
            <YAxis stroke="#94a3b8" tick={{ fontSize: 11 }} />
            <Tooltip contentStyle={{ background: "#101827", border: "1px solid #263244" }} />
            <Area type="monotone" dataKey="traffic" stroke="#34d399" fill="#34d39933" />
          </AreaChart>
        </ResponsiveContainer>
      </Panel>
    </div>
  );
}
