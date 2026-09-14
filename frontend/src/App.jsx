import { useState } from "react";
import Shell from "./layouts/Shell";
import Dashboard from "./pages/Dashboard";
import Copilot from "./pages/Copilot";
import Reports from "./pages/Reports";
import { useLiveData } from "./hooks/useLiveData";

export default function App() {
  const [page, setPage] = useState("dashboard");
  const live = useLiveData();

  return (
    <Shell page={page} onPageChange={setPage} live={live}>
      {page === "dashboard" && <Dashboard live={live} />}
      {page === "copilot" && <Copilot live={live} />}
      {page === "reports" && <Reports />}
    </Shell>
  );
}
