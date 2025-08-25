// src/components/AsinForm.tsx
"use client";

import * as React from "react";
import { analyzeAsins, AnalyzeItem, AnalyzeResponse } from "@/lib/api";

// keep UI state as strings; convert on submit
type Row = {
  asin: string;
  cost: string;            // number-like string
  price_override: string;  // "" or number-like string
  category: string;        // "" or string
  bsr: string;             // "" or number-like string
};

export default function AsinForm({
  onResults,
}: {
  onResults: (res: AnalyzeResponse) => void;
}) {
  const [rows, setRows] = React.useState<Row[]>([
    { asin: "", cost: "", price_override: "", category: "", bsr: "" },
  ]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  function updateRow(i: number, patch: Partial<Row>) {
    setRows((prev) => prev.map((r, idx) => (idx === i ? { ...r, ...patch } : r)));
  }

  function addRow() {
    setRows((prev) => [...prev, { asin: "", cost: "", price_override: "", category: "", bsr: "" }]);
  }

  function removeRow(i: number) {
    setRows((prev) => prev.filter((_, idx) => idx !== i));
  }

  function toNumberOrUndefined(v: string): number | undefined {
    if (v.trim() === "") return undefined;
    const n = Number(v);
    return Number.isFinite(n) ? n : undefined;
  }

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const cleaned: AnalyzeItem[] = rows
        .filter((r) => r.asin.trim() !== "")
        .map((r) => ({
          asin: r.asin.trim(),
          cost: Number(r.cost) || 0,
          price_override: toNumberOrUndefined(r.price_override),
          category: r.category.trim() === "" ? undefined : r.category.trim(),
          bsr: toNumberOrUndefined(r.bsr),
        }));

      const res = await analyzeAsins(cleaned);
      onResults(res);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-3">
      <div className="space-y-2">
        {rows.map((r, i) => (
          <div key={i} className="grid grid-cols-5 gap-2">
            <input
              className="border p-2 rounded"
              placeholder="ASIN"
              value={r.asin}
              onChange={(e) => updateRow(i, { asin: e.target.value })}
            />
            <input
              className="border p-2 rounded"
              placeholder="Cost"
              type="number"
              step="0.01"
              value={r.cost}
              onChange={(e) => updateRow(i, { cost: e.target.value })}
            />
            <input
              className="border p-2 rounded"
              placeholder="Price override (optional)"
              type="number"
              step="0.01"
              value={r.price_override}
              onChange={(e) => updateRow(i, { price_override: e.target.value })}
            />
            <input
              className="border p-2 rounded"
              placeholder="Category (optional)"
              value={r.category}
              onChange={(e) => updateRow(i, { category: e.target.value })}
            />
            <input
              className="border p-2 rounded"
              placeholder="BSR (optional)"
              type="number"
              value={r.bsr}
              onChange={(e) => updateRow(i, { bsr: e.target.value })}
            />
            <div className="col-span-5 text-right">
              {rows.length > 1 && (
                <button
                  type="button"
                  className="text-sm text-red-600"
                  onClick={() => removeRow(i)}
                >
                  Remove row
                </button>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="flex items-center gap-3">
        <button type="button" onClick={addRow} className="px-3 py-2 border rounded">
          + Add row
        </button>
        <button
          type="submit"
          disabled={loading}
          className="px-3 py-2 border rounded bg-black text-white"
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {error && <p className="text-red-600 text-sm">{error}</p>}
    </form>
  );
}
