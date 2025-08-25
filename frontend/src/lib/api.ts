// src/lib/api.ts

export const API_BASE: string =
  process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000/api";

// ---------- Types ----------
export type AnalyzeItem = {
  asin: string;
  cost: number;
  price_override?: number | null;
  category?: string | null;
  bsr?: number | null;
};

export type SimResult = {
  p5: number;
  p50: number;
  p95: number;
  hist?: {
    counts: number[];
    edges: number[];
  };
};

export type AnalyzeRow = {
  asin: string;
  title?: string;
  category?: string;
  price: number;
  cost: number;
  roi: number;
  profit_per_unit: number;
  risk_band: string;
  bsr?: number | null;
  est_monthly_sales: number;
  sim: SimResult;
};

export type AnalyzeResponse = {
  cached: boolean;
  data: AnalyzeRow[];
};

export type UploadCsvPreviewRow = {
  asin: string;
  cost: number;
  price_override?: number | null;
};

export type UploadCsvResponse = {
  ok: boolean;
  count: number;
  preview: UploadCsvPreviewRow[];
};

// ---------- Helpers ----------
async function request<T>(url: string, opts?: RequestInit): Promise<T> {
  const res = await fetch(url, opts);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`HTTP ${res.status}: ${text}`);
  }
  return res.json() as Promise<T>;
}

// ---------- API Calls ----------
export async function health(): Promise<{ ok: boolean }> {
  return request<{ ok: boolean }>(`${API_BASE}/health`, { cache: "no-store" });
}

export async function analyzeAsins(items: AnalyzeItem[]): Promise<AnalyzeResponse> {
  return request<AnalyzeResponse>(`${API_BASE}/asins/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  });
}

export async function uploadCsv(file: File): Promise<UploadCsvResponse> {
  const form = new FormData();
  form.append("file", file);
  return request<UploadCsvResponse>(`${API_BASE}/batches/upload`, {
    method: "POST",
    body: form,
  });
}
