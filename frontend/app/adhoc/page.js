'use client';
import { useEffect, useState } from 'react';
import { api } from '@/lib/api';

export default function AdhocPage() {
  const [datasets, setDatasets] = useState([]);
  const [datasetId, setDatasetId] = useState('');
  const [strategyId, setStrategyId] = useState('');
  const [patientId, setPatientId] = useState('');
  const [patient, setPatient] = useState(null);
  const [preds, setPreds] = useState(null);
  const [log, setLog] = useState('');

  useEffect(()=>{
    api.get('/datasets').then(d=> setDatasets(d.datasets||[])).catch(e=> setLog(e.message));
  }, []);

  async function getRandom() {
    setLog(''); setPatient(null);
    try {
      const data = await api.get(`/adhoc/random?dataset_id=${datasetId}`);
      setPatient(data);
      setPatientId(data.patient_id || '');
    } catch (e) { setLog(e.message); }
  }

  async function predict() {
    setLog(''); setPreds(null);
    try {
      const body = { dataset_id: parseInt(datasetId,10), strategy_id: parseInt(strategyId||'0',10) };
      if (patientId) body.patient_id = patientId;
      const res = await api.post('/adhoc/predict', body);
      setPreds(res);
    } catch (e) { setLog(e.message); }
  }

  return (
    <main className="grid">
      <section className="card">
        <h1 className="title">Ad‑hoc prediction</h1>
        <p className="subtitle">Select dataset & strategy, fetch a random patient, and run predictions. The API returns per‑model JSON.</p>
        <div className="row">
          <div>
            <label className="label">Dataset</label>
            <select className="input" value={datasetId} onChange={e=>setDatasetId(e.target.value)}>
              <option value="">Select…</option>
              {(datasets||[]).map(d=>(<option key={d.id||d.dataset_id} value={d.id||d.dataset_id}>{d.name||d.id}</option>))}
            </select>
          </div>
          <div>
            <label className="label">Strategy ID</label>
            <input className="input" placeholder="e.g. 12" value={strategyId} onChange={e=>setStrategyId(e.target.value)} />
          </div>
          <div>
            <label className="label">Patient ID (optional)</label>
            <input className="input" placeholder="from dataset" value={patientId} onChange={e=>setPatientId(e.target.value)} />
          </div>
        </div>
        <div className="row">
          <button className="btn secondary" onClick={getRandom} disabled={!datasetId}>Fetch Random Patient</button>
          <button className="btn" onClick={predict} disabled={!datasetId || !strategyId}>Predict</button>
        </div>
        {log && <p style={{color:'#ff8'}}>{log}</p>}
      </section>

      {patient && (
        <section className="card">
          <h2 className="title">Patient snapshot</h2>
          <pre className="code">{JSON.stringify(patient, null, 2)}</pre>
        </section>
      )}
      {preds && (
        <section className="card">
          <h2 className="title">Model outputs</h2>
          <pre className="code">{JSON.stringify(preds, null, 2)}</pre>
        </section>
      )}
    </main>
  );
}
