// src/components/BatchUpload.tsx
"use client";

import * as React from "react";
import {
  uploadCsv,
  analyzeAsins,
  type UploadCsvPreviewRow,
  type AnalyzeResponse,
  type AnalyzeRow,
  type AnalyzeItem,
} from "@/lib/api";
import ResultsTable from "@/components/ResultsTable";
import ProfitChart from "@/components/ProfitChart";

export default function BatchUpload() {
  const [preview, setPreview] = React.useState<UploadCsvPreviewRow[] | null>(null);
  const [count, setCount] = React.useState<number>(0);
  const [results, setResults] = React.useState<AnalyzeResponse | null>(null);
  const [selected, setSelected] = React.useState<AnalyzeRow | null>(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  async function onFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    setError(null);
    setResults(null);
    setSelected(null);
    const file = e.target.files?.[0];
    if (!file) return;
    if (!file.name.endsWith(".csv")) {
      setError("Please choose a .csv file.");
      return;
    }
    try {
      setLoading(true);
      const res = await uploadCsv(file);
      setPreview(res.preview);
      setCount(res.count);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Upload failed");
    } finally {
      setLoading(false);
    }
  }

  function downloadSampleCsv() {
    const csv = [
      "asin,cost,price_override",
      "B000TEST01,10.00,25.00",
      "B000TEST02,15.50,32.00",
      "B000TEST03,7.25,19.99",
    ].join("\n");
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "sample_asins.csv";
    a.click();
    URL.revokeObjectURL(url);
  }

  async function analyzePreview() {
    if (!preview || preview.length === 0) return;
    setError(null);
    setLoading(true);
    try {
      const items: AnalyzeItem[] = preview
        .filter((r) => (r.asin || "").trim() !== "")
        .map((r) => ({
          asin: r.asin.trim(),
          cost: Number(r.cost) || 0,
          price_override:
  r.price_override === null || r.price_override === undefined
    ? undefined
    : Number(r.price_override),

          // optional fields not in CSV:
          category: undefined,
          bsr: undefined,
        }));
      const res = await analyzeAsins(items);
      setResults(res);
      setSelected(null);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Analyze failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="space-y-4">
      <div className="flex items-center gap-3">
        <input
          type="file"
          accept=".csv,text/csv"
          onChange={onFileChange}
          className="block"
        />
        <button
          type="button"
          className="px-3 py-2 border rounded"
          onClick={downloadSampleCsv}
        >
          Download sample CSV
        </button>
      </div>

      {loading && <p className="text-sm">Working...</p>}
      {error && <p className="text-sm text-red-600">{error}</p>}

      {preview && (
        <div className="space-y-3">
          <div className="text-sm text-gray-700">
            Previewing first {Math.min(preview.length, 10)} of {count} rows
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full border">
              <thead className="bg-gray-50">
                <tr>
                  <th className="text-left p-2 border-b">ASIN</th>
                  <th className="text-left p-2 border-b">Cost</th>
                  <th className="text-left p-2 border-b">Price override</th>
                </tr>
              </thead>
              <tbody>
                {preview.slice(0, 10).map((r, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="p-2 border-b">{r.asin}</td>
                    <td className="p-2 border-b">{r.cost}</td>
                    <td className="p-2 border-b">{r.price_override ?? ""}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <button
            type="button"
            onClick={analyzePreview}
            disabled={loading}
            className="px-3 py-2 border rounded bg-black text-white"
          >
            {loading ? "Analyzing..." : "Analyze preview"}
          </button>
        </div>
      )}

      {results?.data?.length ? (
        <div className="space-y-3">
          <div className="text-sm">
            {results.cached ? "⚡ Cached result" : "🧮 Fresh computation"}
          </div>
          <ResultsTable rows={results.data} onSelect={setSelected} />
          {selected && (
            <div className="space-y-2">
              <h3 className="text-lg font-semibold">
                Profit bands for {selected.asin}
              </h3>
              <ProfitChart
                label={selected.asin}
                p5={selected.sim.p5}
                p50={selected.sim.p50}
                p95={selected.sim.p95}
              />
            </div>
          )}
        </div>
      ) : null}
    </section>
  );
}
