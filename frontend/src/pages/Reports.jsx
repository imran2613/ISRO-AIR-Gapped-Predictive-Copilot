import { FileDown } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "../services/api";

export default function Reports() {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    api.reports().then(setReports).catch(() => setReports([]));
  }, []);

  return (
    <div className="grid gap-4 md:grid-cols-3">
      {reports.map((report) => (
        <a
          key={report.type}
          href={api.reportUrl(report.type)}
          className="rounded border border-line bg-panel p-5 transition hover:border-cyan hover:shadow-glow"
        >
          <div className="mb-5 grid h-11 w-11 place-items-center rounded bg-cyan/15 text-cyan">
            <FileDown size={22} />
          </div>
          <h3 className="font-semibold">{report.title}</h3>
          <p className="mt-2 text-sm leading-6 text-slate-400">{report.description}</p>
          <p className="mt-5 text-sm font-semibold text-cyan">Download PDF</p>
        </a>
      ))}
    </div>
  );
}
