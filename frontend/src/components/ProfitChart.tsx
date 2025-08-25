// src/components/ProfitChart.tsx
"use client";

import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale, LinearScale, BarElement, Tooltip, Legend,
} from "chart.js";
ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function ProfitChart({
  label,
  p5,
  p50,
  p95,
}: { label: string; p5: number; p50: number; p95: number }) {
  const data = {
    labels: [label],
    datasets: [
      { label: "P5", data: [p5] },
      { label: "P50", data: [p50] },
      { label: "P95", data: [p95] },
    ],
  };
  const options = { responsive: true, plugins: { legend: { position: "top" as const } } };
  return <div className="w-full max-w-md"><Bar data={data} options={options} /></div>;
}
