import Link from 'next/link';

export default function Page() {
  return (
    <main className="grid grid-2">
      <section className="card">
        <h1 className="title">Welcome</h1>
        <p className="subtitle">Start by uploading a dataset, then generate a Gemini‑guided strategy and run ad‑hoc predictions.</p>
        <div className="row">
          <Link className="btn" href="/datasets">Go to Datasets</Link>
          <Link className="btn secondary" href="/strategy">Go to Strategy</Link>
        </div>
      </section>
      <section className="card">
        <h2 className="title">API Base</h2>
        <p className="code">NEXT_PUBLIC_API_BASE = {process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'}</p>
        <small className="muted">Set in <code>.env.local</code> if your backend isn’t on localhost:8000</small>
      </section>
    </main>
  );
}
