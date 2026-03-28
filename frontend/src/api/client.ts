/** Backend base URL. Set VITE_API_URL in .env (e.g. http://127.0.0.1:8000). */
export function getApiBase(): string {
  const raw = import.meta.env.VITE_API_URL as string | undefined;
  return (raw ?? "").replace(/\/$/, "");
}

export async function getHealth(): Promise<{ status: string }> {
  const base = getApiBase();
  const res = await fetch(`${base}/health`);
  if (!res.ok) throw new Error(`GET /health failed: ${res.status}`);
  return res.json() as Promise<{ status: string }>;
}

export async function getApiInfo(): Promise<{ name: string; version: string; docs: string }> {
  const base = getApiBase();
  const res = await fetch(`${base}/api/v1/info`);
  if (!res.ok) throw new Error(`GET /api/v1/info failed: ${res.status}`);
  return res.json() as Promise<{ name: string; version: string; docs: string }>;
}
