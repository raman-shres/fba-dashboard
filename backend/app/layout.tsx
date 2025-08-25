// src/app/layout.tsx
import type { Metadata } from "next";
import type { ReactNode } from "react";   // ✅ import ReactNode
import "./globals.css";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Amazon FBA Analytics Dashboard",
  description: "Analyze ASINs for ROI and risk bands",
};

export default function RootLayout({
  children,
}: { children: ReactNode }) {       // ✅ just ReactNode
  return (
    <html lang="en">
      <body>
        <header className="p-4 border-b bg-white">
          <nav className="max-w-5xl mx-auto flex gap-4">
            <Link href="/" className="font-semibold">Home</Link>
            <Link href="/batch">Batch</Link>
          </nav>
        </header>
        <div className="max-w-5xl mx-auto">{children}</div>
      </body>
    </html>
  );
}
