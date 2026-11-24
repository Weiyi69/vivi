export default function Home() {
  return (
    <div className="min-h-screen bg-background text-primary">
      <header className="border-b border-border bg-white">
        <div className="mx-auto flex h-16 max-w-6xl items-center px-6">
          <span className="text-lg font-semibold text-navy">Vivi</span>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-16">
        <section className="max-w-2xl rounded-2xl border border-border bg-white p-8 shadow-sm">
          <p className="mb-3 text-sm font-semibold uppercase tracking-wide text-primary-blue">
            Foundation
          </p>
          <h1 className="text-3xl font-semibold text-navy">
            Your study workspace starts here.
          </h1>
          <p className="mt-4 leading-7 text-secondary">
            Vivi&apos;s frontend foundation is ready for incremental learning features.
          </p>
        </section>
      </main>
    </div>
  );
}
