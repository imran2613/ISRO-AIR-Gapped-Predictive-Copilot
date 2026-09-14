export default function StatCard({ label, value, tone = "cyan" }) {
  const tones = {
    cyan: "text-cyan border-cyan/30",
    green: "text-emerald-300 border-emerald-400/30",
    amber: "text-amber border-amber/30",
    red: "text-danger border-danger/30"
  };

  return (
    <section className={`rounded border bg-panel p-5 shadow-glow ${tones[tone]}`}>
      <p className="text-sm text-slate-400">{label}</p>
      <div className="mt-3 flex items-end justify-between">
        <strong className="text-4xl font-semibold">{value}</strong>
        <span className="h-3 w-3 rounded-full bg-current status-pulse" />
      </div>
    </section>
  );
}
