import type { ReactNode } from "react";
import Link from "next/link";

export function AuthShell({
  title,
  description,
  children,
}: {
  title: string;
  description: string;
  children: ReactNode;
}) {
  return (
    <main className="min-h-screen bg-background px-6 py-12">
      <div className="mx-auto max-w-md">
        <Link href="/" className="mb-8 block text-xl font-semibold text-navy">
          Vivi
        </Link>
        <section className="rounded-2xl border border-border bg-white p-6 shadow-sm sm:p-8">
          <h1 className="text-2xl font-semibold text-navy">{title}</h1>
          <p className="mt-2 text-sm leading-6 text-secondary">{description}</p>
          <div className="mt-6">{children}</div>
        </section>
      </div>
    </main>
  );
}
