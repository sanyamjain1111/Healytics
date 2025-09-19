'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { api } from '@/lib/api';

export default function DatasetsPage() {
  const [items, setItems] = useState([]);
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  async function load() {
    try {
      const res = await api.get('/datasets');
      setItems(res.datasets || []);
    } catch (e) {
      setError(e.message);
    }
  }
  useEffect(() => { load(); }, []);

  async function upload(e) {
    e.preventDefault();
    if (!file) return;
    setBusy(true); setError('');
    try {
      const fd = new FormData();
      fd.append('file', file);
      const res = await api.upload('/datasets/upload', fd);
      await load();
      alert('Uploaded dataset: ' + (res.dataset?.name || res.dataset?.id));
    } catch (e) {
      setError(e.message);
    } finally { setBusy(false); }
  }

  return (
    <main className="grid">
      <section className="card">
        <h1 className="title">Datasets</h1>
        <p className="subtitle">Upload CSV/Parquet/Feather/XLSX. After upload, the backend persists to Postgres and indexes columns.</p>
        <form onSubmit={upload} className="row" style={{alignItems:'end'}}>
          <div style={{flex:1}}>
            <label className="label">Select file</label>
            <input className="input" type="file" onChange={e=>setFile(e.target.files?.[0]||null)} />
          </div>
          <button className="btn" disabled={busy}>{busy?'Uploading…':'Upload'}</button>
        </form>
        {error && <p style={{color:'#ff8'}}>{error}</p>}
      </section>

      <section className="card">
        <h2 className="title">Available datasets</h2>
        <div className="table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Name</th><th>Rows</th><th>Actions</th></tr></thead>
            <tbody>
              {(items||[]).map((d, i)=> (
                <tr key={d.id||i}>
                  <td>{d.id||d.dataset_id||i}</td>
                  <td>{d.name||'-'}</td>
                  <td>{d.rows||d.row_count||'-'}</td>
                  <td><Link href={`/datasets/${d.id||d.dataset_id}`}>Open</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}
