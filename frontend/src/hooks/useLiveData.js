import { useEffect, useState } from "react";
import { api } from "../services/api";

export function useLiveData(intervalMs = 3500) {
  const [data, setData] = useState({ routers: [], alerts: [], metrics: null, predictions: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [trigger, setTrigger] = useState(0);

  const refresh = () => setTrigger((t) => t + 1);

  useEffect(() => {
    let active = true;

    async function load() {
      try {
        const [routers, alerts, metrics, predictions] = await Promise.all([
          api.routers(),
          api.alerts(),
          api.metrics(),
          api.predictions()
        ]);
        if (active) {
          setData({ routers, alerts, metrics, predictions });
          setError("");
          setLoading(false);
        }
      } catch (err) {
        if (active) {
          setError(err.message);
          setLoading(false);
        }
      }
    }

    load();
    const timer = setInterval(load, intervalMs);
    return () => {
      active = false;
      clearInterval(timer);
    };
  }, [intervalMs, trigger]);

  return { ...data, loading, error, refresh };
}
