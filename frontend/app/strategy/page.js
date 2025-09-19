'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function StrategyPage() {
  const [datasets, setDatasets] = useState([]);
  const [datasetId, setDatasetId] = useState('');
  const [strategy, setStrategy] = useState(null);
  const [fallback, setFallback] = useState([]);
  const [error, setError] = useState('');

  useEffect(()=>{
    api.get('/datasets').then(d=> setDatasets(d.datasets||[])).catch(e=> setError(e.message));
    api.get('/strategies').then(d=> setFallback(d.strategies||[])).catch(()=>{});
  }, []);

  async function generate() {
    setError(''); setStrategy(null);
    try {
      const s = await api.post('/strategy/generate', { dataset_id: datasetId });
      setStrategy(s);
    } catch (e) {
      setError('Falling back to static strategies (no /strategy/generate)');
      setStrategy({ strategies: fallback });
    }
  }

  return (
    <main className="grid">
      <section className="card">
        <h1 className="title">Strategy</h1>
        <p className="subtitle">Pick a dataset, call Gemini strategist, and view the plan (models, thresholds, preprocessing).</p>
        <div className="row">
          <div>
            <label className="label">Dataset</label>
            <select className="input" value={datasetId} onChange={e=>setDatasetId(e.target.value)}>
              <option value="">Select…</option>
              {(datasets||[]).map(d=>(<option key={d.id||d.dataset_id} value={d.id||d.dataset_id}>{d.name||d.id}</option>))}
            </select>
          </div>
          <button className="btn" onClick={generate} disabled={!datasetId}>Generate Strategy</button>
        </div>
      </section>

      {strategy && (
        <section className="card">
          <h2 className="title">Result</h2>
          <p className="subtitle">Copy the <b>strategy_id</b> (or model list) into Ad‑hoc.</p>
          <pre className="code">{JSON.stringify(strategy, null, 2)}</pre>
        </section>
      )}

      {error && <p style={{color:'#ff8'}}>{error}</p>}
    </main>
  );
}
