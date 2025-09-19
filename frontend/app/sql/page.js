'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function SQLPage() {
  const [datasets, setDatasets] = useState([]);
  const [datasetId, setDatasetId] = useState('');
  const [sql, setSQL] = useState('select * from df limit 10');
  const [rows, setRows] = useState([]);
  const [cols, setCols] = useState([]);
  const [err, setErr] = useState('');

  useEffect(()=>{
    api.get('/datasets').then(d=> setDatasets(d.datasets||[])).catch(e=> setErr(e.message));
  }, []);

  async function run() {
    setErr('');
    try {
      const res = await api.post('/analytics/ad-hoc', { dataset_id: datasetId, sql });
      setCols(res.columns || []);
      setRows(res.rows || []);
    } catch (e) { setErr(e.message); }
  }

  return (
    <main className="grid">
      <section className="card">
        <h1 className="title">SQL (DuckDB)</h1>
        <p className="subtitle">Query the uploaded dataset in‑browser by calling your backend’s DuckDB runner.</p>
        <div className="row">
          <div>
            <label className="label">Dataset</label>
            <select className="input" value={datasetId} onChange={e=>setDatasetId(e.target.value)}>
              <option value="">Select…</option>
              {(datasets||[]).map(d=>(<option key={d.id||d.dataset_id} value={d.id||d.dataset_id}>{d.name||d.id}</option>))}
            </select>
          </div>
        </div>
        <div style={{marginTop:12}}>
          <label className="label">SQL</label>
          <textarea className="input" rows={6} value={sql} onChange={e=>setSQL(e.target.value)} />
        </div>
        <button className="btn" style={{marginTop:12}} onClick={run} disabled={!datasetId}>Run</button>
        {err && <p style={{color:'#ff8'}}>{err}</p>}
      </section>

      {(rows.length>0) && (
        <section className="card">
          <h2 className="title">Results</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>{cols.map(c=>(<th key={c}>{c}</th>))}</tr>
              </thead>
              <tbody>
                {rows.map((r,i)=>(
                  <tr key={i}>
                    {r.map((v,j)=>(<td key={j}>{String(v)}</td>))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      )}
    </main>
  );
}
