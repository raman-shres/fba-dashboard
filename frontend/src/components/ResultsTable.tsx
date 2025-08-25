// src/components/ResultsTable.tsx
"use client";

import * as React from "react";
import {
  ColumnDef, getCoreRowModel, getSortedRowModel,
  flexRender, SortingState, useReactTable,
} from "@tanstack/react-table";
import type { AnalyzeRow } from "@/lib/api";

export default function ResultsTable({
  rows, onSelect,
}: { rows: AnalyzeRow[]; onSelect?: (r: AnalyzeRow) => void }) {
  const [sorting, setSorting] = React.useState<SortingState>([{ id: "roi", desc: true }]);

  const columns = React.useMemo<ColumnDef<AnalyzeRow>[]>(() => [
    { header: "ASIN", accessorKey: "asin" },
    { header: "Title", accessorKey: "title" },
    { header: "Category", accessorKey: "category" },
    { header: "Price", accessorKey: "price",
      cell: info => info.getValue<number>().toFixed(2) },
    { header: "Cost", accessorKey: "cost",
      cell: info => info.getValue<number>().toFixed(2) },
    { header: "ROI", accessorKey: "roi",
      cell: info => (info.getValue<number>() * 100).toFixed(1) + "%" },
    { header: "Profit/Unit", accessorKey: "profit_per_unit",
      cell: info => info.getValue<number>().toFixed(2) },
    { header: "Risk", accessorKey: "risk_band" },
    { header: "BSR", accessorKey: "bsr" },
    { header: "Est Sales/mo", accessorKey: "est_monthly_sales" },
  ], []);

  const table = useReactTable({
    data: rows, columns,
    state: { sorting },
    onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(),
    getSortedRowModel: getSortedRowModel(),
  });

  return (
    <div className="w-full overflow-x-auto">
      <table className="min-w-full border">
        <thead className="bg-gray-50">
          {table.getHeaderGroups().map(hg => (
            <tr key={hg.id}>
              {hg.headers.map(h => (
                <th key={h.id}
                    className="text-left p-2 border-b cursor-pointer select-none"
                    onClick={h.column.getToggleSortingHandler()}>
                  {flexRender(h.column.columnDef.header, h.getContext())}
                  {{ asc: " ▲", desc: " ▼" }[h.column.getIsSorted() as string] ?? null}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(r => (
            <tr key={r.id}
                className="hover:bg-gray-50"
                onClick={() => onSelect?.(r.original)}>
              {r.getVisibleCells().map(c => (
                <td key={c.id} className="p-2 border-b">
                  {flexRender(c.column.columnDef.cell, c.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
