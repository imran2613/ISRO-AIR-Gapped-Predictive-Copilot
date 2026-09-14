const API_BASE = import.meta.env.VITE_API_BASE || "/api";

async function request(path, options) {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options
  });
  if (!response.ok) {
    throw new Error(`API ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export const api = {
  routers: () => request("/routers"),
  alerts: () => request("/alerts"),
  metrics: () => request("/metrics"),
  predictions: () => request("/predictions"),
  reports: () => request("/reports"),
  chat: (message) => request("/chat", { method: "POST", body: JSON.stringify({ message }) }),
  reportUrl: (type) => `${API_BASE}/reports/${type}`,
  importRouters: (data) => request("/routers/import", { method: "POST", body: JSON.stringify(data) }),
  resetRouters: () => request("/routers/reset", { method: "POST" })
};
