import { Activity, Bot, FileDown, RadioTower, ShieldCheck, Upload, RotateCcw } from "lucide-react";
import { api } from "../services/api";

const nav = [
  { id: "dashboard", label: "Operations", icon: Activity },
  { id: "copilot", label: "AI Copilot", icon: Bot },
  { id: "reports", label: "Reports", icon: FileDown }
];

export default function Shell({ children, page, onPageChange, live }) {
  const critical = live.metrics?.summary?.critical_routers || 0;

  const handleImportCSV = (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = async (evt) => {
      const text = evt.target.result;
      const lines = text.split("\n").map(l => l.trim()).filter(Boolean);
      if (lines.length < 2) return;
      const headers = lines[0].split(",").map(h => h.trim().toLowerCase());
      const data = [];
      for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(",").map(v => v.trim());
        const row = {};
        headers.forEach((h, index) => {
          row[h] = values[index];
        });
        if (row.cpu && row.memory) {
          data.push({
            router_id: row.router_id || `Custom-R${i}`,
            site: row.site || `Custom Site ${i}`,
            cpu: parseFloat(row.cpu) || 0.0,
            memory: parseFloat(row.memory) || 0.0,
            latency: parseFloat(row.latency) || 0.0,
            packet_loss: parseFloat(row.packet_loss) || 0.0,
            bandwidth: parseFloat(row.bandwidth) || 0.0,
          });
        }
      }
      if (data.length > 0) {
        try {
          await api.importRouters(data);
          if (live && live.refresh) {
            live.refresh();
          }
        } catch (err) {
          alert("Import failed: " + err.message);
        }
      } else {
        alert("No valid rows containing CPU and memory columns were found in the CSV.");
      }
    };
    reader.readAsText(file);
    // Reset file input value so same file can be selected again
    e.target.value = "";
  };

  const handleReset = async () => {
    try {
      await api.resetRouters();
      if (live && live.refresh) {
        live.refresh();
      }
    } catch (err) {
      alert("Reset failed: " + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-space text-slate-100">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-64 border-r border-line bg-[#0b111d] p-4 lg:block">
        <div className="flex items-center gap-3 border-b border-line pb-5">
          <div className="grid h-11 w-11 place-items-center rounded bg-cyan/15 text-cyan">
            <RadioTower size={24} />
          </div>
          <div>
            <p className="text-sm font-semibold uppercase tracking-wider text-cyan">ISRO BAH 2026</p>
            <h1 className="text-lg font-semibold leading-tight">MPLS Copilot</h1>
          </div>
        </div>

        <nav className="mt-6 space-y-2">
          {nav.map((item) => {
            const Icon = item.icon;
            const active = page === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onPageChange(item.id)}
                className={`flex h-11 w-full items-center gap-3 rounded px-3 text-left text-sm transition ${
                  active ? "bg-cyan text-slate-950" : "text-slate-300 hover:bg-slate-800"
                }`}
              >
                <Icon size={18} />
                {item.label}
              </button>
            );
          })}
        </nav>

        <div className="absolute bottom-4 left-4 right-4 rounded border border-line bg-panel p-4">
          <div className="flex items-center gap-2 text-sm font-medium">
            <ShieldCheck size={18} className="text-cyan" />
            Air-gapped mode
          </div>
          <p className="mt-2 text-xs leading-5 text-slate-400">Offline simulator, local ML model, SQLite audit trail.</p>
        </div>
      </aside>

      <main className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-line bg-space/90 px-4 py-4 backdrop-blur md:px-8">
          <div className="flex flex-col justify-between gap-3 md:flex-row md:items-center">
            <div>
              <p className="text-xs font-semibold uppercase tracking-widest text-cyan">Secure MPLS Operations</p>
              <h2 className="text-2xl font-semibold">Air-Gapped Predictive Copilot</h2>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              {live.metrics?.is_custom_mode && (
                <div className="rounded border border-amber-500/30 bg-amber-500/10 px-3 py-2 text-sm text-amber-400">
                  Custom Data Mode
                </div>
              )}
              <label className="flex cursor-pointer items-center gap-2 rounded border border-line bg-panel px-3 py-2 text-sm hover:bg-slate-800 transition text-cyan">
                <Upload size={16} />
                <span>Import CSV</span>
                <input
                  type="file"
                  accept=".csv"
                  className="hidden"
                  onChange={handleImportCSV}
                />
              </label>
              {live.metrics?.is_custom_mode && (
                <button
                  onClick={handleReset}
                  className="flex items-center gap-2 rounded border border-line bg-panel px-3 py-2 text-sm hover:bg-slate-800 transition text-rose-400 hover:text-rose-350"
                >
                  <RotateCcw size={16} />
                  <span>Reset Sim</span>
                </button>
              )}
              <div className="flex items-center gap-2 rounded border border-line bg-panel px-3 py-2 text-sm">
                <span className={`h-2.5 w-2.5 rounded-full ${critical ? "bg-danger" : "bg-cyan"} status-pulse`} />
                {critical ? `${critical} critical routers` : "Network stable"}
              </div>
              <div className="rounded border border-line bg-panel px-3 py-2 text-sm text-slate-300">
                Live telemetry every 3.5s
              </div>
            </div>
          </div>
        </header>
        <div className="p-4 md:p-8">{children}</div>
      </main>
    </div>
  );
}
