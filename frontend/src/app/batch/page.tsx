// src/app/batch/page.tsx
"use client";

import * as React from "react";
import BatchUpload from "@/components/BatchUpload";

export default function BatchPage() {
  return (
    <main className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Batch Analyze (CSV)</h1>
      <p className="text-sm text-gray-600">
        Upload a CSV with headers: <code>asin,cost,price_override</code>
      </p>
      <BatchUpload />
    </main>
  );
}
