export default function PredictionPanel({ predictions = [], routers = [] }) {
  const routerById = Object.fromEntries(routers.map((router) => [router.router_id, router]));

  return (
    <section className="rounded border border-line bg-panel p-4">
      <h3 className="font-semibold">Predictive Failure Engine</h3>
      <div className="mt-4 space-y-4">
        {predictions.slice(0, 5).map((prediction) => {
          const router = routerById[prediction.router_id];
          return (
            <div key={prediction.router_id} className="rounded border border-line bg-slate-950/35 p-3">
              <div className="flex items-center justify-between gap-3">
                <div>
                  <p className="font-semibold text-cyan">{prediction.router_id}</p>
                  <p className="text-xs text-slate-400">{router?.site}</p>
                </div>
                <span className="text-sm font-semibold">{prediction.risk_score.toFixed(1)}</span>
              </div>
              <div className="mt-3 h-2 rounded bg-slate-800">
                <div
                  className="h-2 rounded bg-cyan"
                  style={{ width: `${Math.min(100, prediction.risk_score)}%` }}
                />
              </div>
              <p className="mt-2 text-xs text-slate-400">
                {prediction.predicted_state} · {(prediction.failure_probability * 100).toFixed(1)}% failure probability
              </p>
              <p className="mt-2 text-sm text-slate-300">{router?.root_cause}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}
