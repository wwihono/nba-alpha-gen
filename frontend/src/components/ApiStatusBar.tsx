import { useEffect, useState } from "react";
import { getApiBase, getApiInfo, getHealth } from "../api/client";

type Status = "idle" | "loading" | "ok" | "error";

export function ApiStatusBar() {
  const base = getApiBase();
  const [status, setStatus] = useState<Status>(() => (base ? "loading" : "idle"));
  const [detail, setDetail] = useState<string>("");

  useEffect(() => {
    if (!base) return;

    let cancelled = false;

    Promise.all([getHealth(), getApiInfo()])
      .then(([h, info]) => {
        if (cancelled) return;
        setStatus("ok");
        setDetail(`${info.name} v${info.version} · ${h.status}`);
      })
      .catch((e: unknown) => {
        if (cancelled) return;
        setStatus("error");
        setDetail(e instanceof Error ? e.message : "Connection failed");
      });

    return () => {
      cancelled = true;
    };
  }, [base]);

  if (!base) {
    return (
      <div className="api-status api-status--error" role="status">
        <span className="api-status__dot" aria-hidden />
        <span className="api-status__label">API offline</span>
        <span className="api-status__detail">
          Set VITE_API_URL in frontend/.env (e.g. http://127.0.0.1:8000)
        </span>
      </div>
    );
  }

  return (
    <div className={`api-status api-status--${status}`} role="status">
      <span className="api-status__dot" aria-hidden />
      <span className="api-status__label">
        {status === "idle" && "API"}
        {status === "loading" && "Connecting to API…"}
        {status === "ok" && "API"}
        {status === "error" && "API offline"}
      </span>
      {detail ? <span className="api-status__detail">{detail}</span> : null}
    </div>
  );
}
