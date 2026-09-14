const statusClass = {
  Healthy: "bg-emerald-400/10 text-emerald-300",
  Warning: "bg-amber/10 text-amber",
  Critical: "bg-danger/10 text-danger"
};

export default function RouterTable({ routers = [] }) {
  return (
    <section className="overflow-hidden rounded border border-line bg-panel">
      <div className="border-b border-line p-4">
        <h3 className="font-semibold">Router Operations Table</h3>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full min-w-[900px] text-left text-sm">
          <thead className="bg-slate-900 text-xs uppercase tracking-wider text-slate-400">
            <tr>
              <th className="px-4 py-3">Router</th>
              <th className="px-4 py-3">Site</th>
              <th className="px-4 py-3">Status</th>
              <th className="px-4 py-3">CPU</th>
              <th className="px-4 py-3">Memory</th>
              <th className="px-4 py-3">Latency</th>
              <th className="px-4 py-3">Loss</th>
              <th className="px-4 py-3">Bandwidth</th>
              <th className="px-4 py-3">Last Updated</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {routers.map((router) => (
              <tr key={router.router_id} className="hover:bg-slate-900/60">
                <td className="px-4 py-3 font-semibold text-cyan">{router.router_id}</td>
                <td className="px-4 py-3 text-slate-300">{router.site}</td>
                <td className="px-4 py-3">
                  <span className={`rounded px-2 py-1 text-xs font-semibold ${statusClass[router.status]}`}>
                    {router.status}
                  </span>
                </td>
                <td className="px-4 py-3">{router.cpu.toFixed(1)}%</td>
                <td className="px-4 py-3">{router.memory.toFixed(1)}%</td>
                <td className="px-4 py-3">{router.latency.toFixed(1)} ms</td>
                <td className="px-4 py-3">{router.packet_loss.toFixed(2)}%</td>
                <td className="px-4 py-3">{router.bandwidth.toFixed(1)}%</td>
                <td className="px-4 py-3 text-slate-400">{new Date(router.last_updated).toLocaleTimeString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
