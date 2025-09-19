'use client';
import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { api } from '@/lib/api';
import { Histogram } from '@/components/Histogram';

export default function DatasetDetail() {
  const params = useParams();
  const id = params.id;
  const [summary, setSummary] = useState(null);
  const [columns, setColumns] = useState([]);
  const [chosen, setChosen] = useState('');
  const [hists, setHists] = useState([]);
  const [error, setError] = useState('');

  async function loadSummary() {
    try {
      const s = await api.get(`/datasets/${id}/summary`);
      setSummary(s);
      const cols = await api.get(`/datasets/${id}/columns`);
      setColumns(cols.columns || []);
    } catch (e) { setError(e.message); }
  }

  async function loadHists() {
    if (!chosen) return;
    try {
      const qs = new URLSearchParams({ dataset_id: id, columns: chosen, bins: '20' });
      const res = await api.get(`/analytics/histograms?${qs.toString()}`);
      setHists(res.histograms || []);
    } catch (e) { setError(e.message); }
  }

  useEffect(()=>{ loadSummary(); }, [id]);

  return (
    <main className="grid">
      <section className="card">
        <h1 className="title">Dataset #{id}</h1>
        {error && <p style={{color:'#ff8'}}>{error}</p>}
        {summary && (
          <div className="row">
            <div className="card" style={{flex:1}}>
              <h3>Meta</h3>
              <div className="table-wrap"><table>
                <tbody>
                  <tr><td>Rows</td><td>{summary.meta?.rows}</td></tr>
                  <tr><td>Columns</td><td>{summary.meta?.columns}</td></tr>
                  <tr><td>Missing %</td><td>{summary.meta?.missing_ratio}</td></tr>
                </tbody>
              </table></div>
            </div>
            <div className="card" style={{flex:2}}>
              <h3>Sample (first 10)</h3>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>{(summary.sample?.columns||[]).map(c=>(<th key={c}>{c}</th>))}</tr>
                  </thead>
                  <tbody>
                    {(summary.sample?.rows||[]).map((r,i)=>(
                      <tr key={i}>{r.map((v,j)=>(<td key={j}>{String(v)}</td>))}</tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </section>

      <section className="card">
        <h2 className="title">Histograms</h2>
        <div className="row" style={{alignItems:'end'}}>
          <div style={{flex:1}}>
            <label className="label">Pick columns (comma‑separated, numeric)</label>
            <input className="input" placeholder="e.g. age,heart_rate,glucose" value={chosen} onChange={e=>setChosen(e.target.value)} />
          </div>
          <button className="btn" onClick={loadHists}>Generate</button>
        </div>
        <hr className="sep" />
        <div className="grid grid-3">
          {hists.map((h, idx)=> (<Histogram key={idx} hist={h} />))}
        </div>
      </section>
    </main>
  );
}
