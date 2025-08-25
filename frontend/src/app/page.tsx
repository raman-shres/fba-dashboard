// src/app/page.tsx
"use client";

import * as React from "react";
import { health, type AnalyzeResponse, type AnalyzeRow } from "@/lib/api";
import AsinForm from "@/components/AsinForm";
import ResultsTable from "@/components/ResultsTable";
import ProfitChart from "@/components/ProfitChart";

export default function Home() {
  const [apiOk, setApiOk] = React.useState<boolean | null>(null);
  const [results, setResults] = React.useState<AnalyzeResponse | null>(null);
  const [selected, setSelected] = React.useState<AnalyzeRow | null>(null);

  React.useEffect(() => {
    health().then(() => setApiOk(true)).catch(() => setApiOk(false));
  }, []);

  return (
    <main className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Amazon FBA Analytics Dashboard</h1>

      <div className="text-sm">
        API status: {apiOk === null ? "checking..." : apiOk ? "✅ healthy" : "❌ cannot reach API"}
      </div>

      <section className="space-y-3">
        <h2 className="text-xl font-semibold">Analyze ASINs</h2>
        <AsinForm onResults={(res) => { setResults(res); setSelected(null); }} />
      </section>

      {results?.data?.length ? (
        <section className="space-y-3">
          <h2 className="text-xl font-semibold">Results</h2>
          <ResultsTable
            rows={results.data}
            onSelect={(row) => setSelected(row)}
          />
        </section>
      ) : null}

      {selected ? (
        <section className="space-y-3">
          <h2 className="text-xl font-semibold">Profit bands for {selected.asin}</h2>
          <ProfitChart
            label={selected.asin}
            p5={selected.sim.p5}
            p50={selected.sim.p50}
            p95={selected.sim.p95}
          />
        </section>
      ) : null}
    </main>
  );
}
