import React, { useState, useMemo, useRef } from 'react';
import { BarChart3, Activity, AlertTriangle, Loader2, CheckCircle, AlertCircle, Navigation, ChevronDown } from 'lucide-react';
import { api, fetchArtifact } from '../api';
import RiskHistogram from './RiskHistogram';
import RegressorHistogram from './RegressorHistogram';
import SummaryReadable from './SummaryReadable';

const CLASSIFIERS = new Set([
  "DiseaseRiskPredictor","ReadmissionPredictor","Readmission90DPredictor",
  "MortalityRiskModel","ICUAdmissionPredictor","SepsisEarlyWarning",
  "DiabetesComplicationRisk","HypertensionControlPredictor",
  "HeartFailure30DRisk","StrokeRiskPredictor","COPDExacerbationPredictor",
  "AKIRiskPredictor","AdverseDrugEventPredictor","NoShowAppointmentPredictor"
]);
const REGRESSORS = new Set(["LengthOfStayRegressor","CostOfCareRegressor","AnemiaSeverityRegressor"]);

function NavigationBar({ modelNames, onNavigate }) {
  if (modelNames.length === 0) return null;

  const handleScrollTo = (modelName) => {
    const element = document.getElementById(`model-${modelName}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    onNavigate?.(modelName);
  };

  const handleScrollToSummary = () => {
    const element = document.getElementById('summary-section');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const handleScrollToAnomalies = () => {
    const element = document.getElementById('anomalies-section');
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <div className="sticky top-0 z-10 bg-white/90 backdrop-blur-sm border-b border-purple-200 shadow-lg">
      <div className="px-6 py-4">
        <div className="flex items-center gap-2 mb-3">
          <Navigation className="w-4 h-4 text-violet-600" />
          <div className="text-sm font-semibold text-gray-700">Navigate to:</div>
        </div>
        <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto">
          <button
            onClick={handleScrollToSummary}
            className="flex items-center gap-2 px-4 py-2 text-sm bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-800 rounded-xl hover:from-blue-200 hover:to-cyan-200 transition-all duration-200 font-medium border border-blue-200 shadow-sm hover:shadow-md"
          >
            <BarChart3 className="w-4 h-4" />
            Summary
          </button>
          {modelNames.map(modelName => (
            <button
              key={modelName}
              onClick={() => handleScrollTo(modelName)}
              className={`flex items-center gap-2 px-4 py-2 text-sm rounded-xl transition-all duration-200 font-medium border shadow-sm hover:shadow-md ${
                CLASSIFIERS.has(modelName)
                  ? 'bg-gradient-to-r from-violet-100 to-purple-100 text-violet-800 hover:from-violet-200 hover:to-purple-200 border-violet-200'
                  : 'bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-800 hover:from-emerald-200 hover:to-teal-200 border-emerald-200'
              }`}
            >
              {CLASSIFIERS.has(modelName) ? <Activity className="w-4 h-4" /> : <BarChart3 className="w-4 h-4" />}
              {modelName}
            </button>
          ))}
          <button
            onClick={handleScrollToAnomalies}
            className="flex items-center gap-2 px-4 py-2 text-sm bg-gradient-to-r from-orange-100 to-red-100 text-orange-800 rounded-xl hover:from-orange-200 hover:to-red-200 transition-all duration-200 font-medium border border-orange-200 shadow-sm hover:shadow-md"
          >
            <AlertTriangle className="w-4 h-4" />
            Anomalies
          </button>
        </div>
      </div>
    </div>
  );
}

function HighRiskTable({ data, modelName, isOpen, onToggle }) {
  const highRiskPatients = data.filter(r => {
    if (r.threshold != null && r.score != null) {
      return r.score >= r.threshold;
    }
    if (r.pred != null) {
      return r.pred === 1 || r.pred === true || r.pred === 'high';
    }
    if (r.score != null) {
      return r.score >= 0.5;
    }
    return false;
  }).sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 20);
  
  console.log(`${modelName}: isOpen=${isOpen}, highRiskPatients=${highRiskPatients.length}`);
  
  if (highRiskPatients.length === 0) {
    return (
      <div className="mt-6 p-4 bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200 rounded-xl">
        <div className="text-sm text-green-700 font-medium">No high-risk patients identified for {modelName}</div>
      </div>
    );
  }

  return (
    <div className="mt-6">
      <button 
        onClick={(e) => {
          e.preventDefault();
          console.log(`Clicking toggle for ${modelName}, current state: ${isOpen}`);
          onToggle();
        }}
        className="group flex items-center gap-3 text-lg font-semibold text-gray-800 hover:text-violet-700 transition-colors mb-4 cursor-pointer bg-gradient-to-r from-white to-gray-50 p-3 rounded-xl border border-gray-200 hover:border-violet-300 w-full"
        type="button"
      >
        <AlertTriangle className="w-5 h-5 text-orange-500" />
        <span>High Risk Patients ({highRiskPatients.length})</span>
        <ChevronDown 
          className={`w-5 h-5 text-gray-400 transition-transform duration-200 ml-auto ${
            isOpen ? 'rotate-180' : 'rotate-0'
          }`}
        />
      </button>
      
      {isOpen && (
        <div className="bg-white border border-gray-200 rounded-2xl overflow-hidden shadow-lg">
          <div className="overflow-auto">
            <table className="min-w-full text-sm">
              <thead className="bg-gradient-to-r from-red-500 to-orange-500 text-white">
                <tr>
                  <th className="text-left p-4 font-semibold">Patient ID</th>
                  <th className="text-left p-4 font-semibold">Risk Score</th>
                  <th className="text-left p-4 font-semibold">Prediction</th>
                  <th className="text-left p-4 font-semibold">Threshold</th>
                </tr>
              </thead>
              <tbody>
                {highRiskPatients.map((r, i) => (
                  <tr key={`${r.patient_id}-${i}`} className="border-b border-gray-100 last:border-0 hover:bg-red-50 transition-colors">
                    <td className="p-4 font-mono font-medium text-gray-800">{r.patient_id}</td>
                    <td className="p-4">
                      {r.score != null ? (
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          r.score >= 0.8 ? 'bg-red-100 text-red-800' :
                          r.score >= 0.6 ? 'bg-orange-100 text-orange-800' :
                          r.score >= 0.4 ? 'bg-yellow-100 text-yellow-800' :
                          'bg-green-100 text-green-800'
                        }`}>
                          {r.score.toFixed(3)}
                        </span>
                      ) : (
                        <span className="text-gray-400">N/A</span>
                      )}
                    </td>
                    <td className="p-4">
                      <span className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-xs font-semibold">
                        {r.pred != null ? String(r.pred) : 'High Risk'}
                      </span>
                    </td>
                    <td className="p-4">
                      {r.threshold != null ? (
                        <span className="text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">{r.threshold.toFixed(3)}</span>
                      ) : (
                        <span className="text-gray-400">N/A</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default function AnalysisPage() {
  const [datasetId, setDatasetId] = useState('');
  const [strategyId, setStrategyId] = useState('');
  const [running, setRunning] = useState(false);
  const [summary, setSummary] = useState(null);
  const [risk, setRisk] = useState(null);
  const [anom, setAnom] = useState(null);
  const [err, setErr] = useState('');
  const [openTables, setOpenTables] = useState({});
  const [activeModel, setActiveModel] = useState(null);

  const toggleTable = (modelName) => {
    console.log(`toggleTable called for ${modelName}`);
    console.log('Current openTables:', openTables);
    
    setOpenTables(prev => {
      const newState = {
        ...prev,
        [modelName]: !prev[modelName]
      };
      console.log('New openTables state:', newState);
      return newState;
    });
  };

  async function run() {
    setErr('');
    setRunning(true);
    setSummary(null); setRisk(null); setAnom(null);
    setOpenTables({});
    try {
      const client = api();
      const payload = { dataset_id: Number(datasetId) };
      if (strategyId) payload.strategy_id = Number(strategyId);
      const r = await client.post('/analytics/run', payload);
      setSummary(r.data?.summary || null);

      const riskPath = r.data?.risk_json;
      const anomPath = r.data?.anomaly_json;
      const riskData = riskPath ? await fetchArtifact(riskPath) : null;
      const anomData = anomPath ? await fetchArtifact(anomPath) : null;
      setRisk(riskData);
      setAnom(anomData);
    } catch (e) {
      setErr('Failed to run analysis.');
    } finally {
      setRunning(false);
    }
  }

  const modelLists = useMemo(() => {
    const out = {};
    if (!risk || !risk.patients) return out;
    for (const entry of risk.patients) {
      const pid = entry.patient_id;
      for (const [k, v] of Object.entries(entry)) {
        if (k === 'patient_id') continue;
        if (!out[k]) out[k] = [];
        if (v && typeof v === 'object' && 'score' in v) {
          out[k].push({ patient_id: pid, score: v.score, pred: v.pred, threshold: v.threshold });
        } else if (v && typeof v === 'object' && 'prediction' in v) {
          out[k].push({ patient_id: pid, prediction: v.prediction });
        }
      }
    }
    return out;
  }, [risk]);

  const isError = err.includes('failed') || err.includes('Failed');

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl shadow-lg">
              <Activity className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              Analytics Engine
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Run comprehensive ML analysis on your datasets</p>
        </div>

        {/* Input Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 mb-8 hover:shadow-2xl transition-all duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Run Analysis</h2>
          </div>

          <div className="grid md:grid-cols-4 gap-6 items-end">
            <div className="space-y-3">
              <label className="block text-sm font-semibold text-gray-700">Dataset ID</label>
              <input 
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-violet-400 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80"
                value={datasetId} 
                onChange={e => setDatasetId(e.target.value)}
                placeholder="Enter dataset ID..."
              />
            </div>
            <div className="space-y-3">
              <label className="block text-sm font-semibold text-gray-700">Strategy ID (optional)</label>
              <input 
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-violet-400 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80"
                value={strategyId} 
                onChange={e => setStrategyId(e.target.value)}
                placeholder="Enter strategy ID..."
              />
            </div>
            <div className="md:col-span-2">
              <button 
                className={`w-full py-4 px-6 rounded-2xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 ${
                  running || !datasetId 
                    ? 'bg-gray-400 cursor-not-allowed' 
                    : 'bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                }`}
                onClick={run} 
                disabled={running || !datasetId}
              >
                {running ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Running Analysis...
                  </>
                ) : (
                  <>
                    <Activity className="w-5 h-5" />
                    Run Analysis
                  </>
                )}
              </button>
            </div>
          </div>

          {err && (
            <div className="mt-6 p-4 rounded-2xl flex items-center gap-3 bg-red-50 border border-red-200 text-red-700">
              <AlertCircle className="w-5 h-5 text-red-500" />
              <span className="text-sm font-medium">{err}</span>
            </div>
          )}
        </div>

        {(summary || risk) && (
          <NavigationBar 
            modelNames={Object.keys(modelLists)} 
            onNavigate={setActiveModel}
          />
        )}

        {summary && (
          <div id="summary-section" className="mb-8">
            <SummaryReadable summary={summary} />
          </div>
        )}

        {risk && (
          <div className="space-y-8 mb-8">
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl">
                  <BarChart3 className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800">Model Results</h2>
              </div>
              
              <div className="space-y-10">
                {Object.keys(modelLists).map(m => {
                  const rows = modelLists[m];
                  if (CLASSIFIERS.has(m)) {
                    const scores = rows.map(r => r.score).filter(x => typeof x === 'number');
                    const thr = rows.find(r => r.threshold != null)?.threshold ?? null;
                    return (
                      <div key={m} id={`model-${m}`} className="scroll-mt-20 bg-gradient-to-br from-white to-violet-50 border border-violet-200 rounded-2xl p-6 hover:shadow-lg transition-all duration-200">
                        <div className="flex items-center gap-3 mb-4">
                          <div className="p-2 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl">
                            <Activity className="w-5 h-5 text-white" />
                          </div>
                          <h3 className="text-xl font-bold text-gray-800">{m}</h3>
                          <span className="text-sm bg-violet-100 text-violet-700 px-3 py-1 rounded-full font-semibold">classifier</span>
                        </div>
                        <RiskHistogram scores={scores} threshold={thr} title={`${m} — Score Distribution`} />
                        <HighRiskTable 
                          data={rows} 
                          modelName={m}
                          isOpen={openTables[m] || false}
                          onToggle={() => toggleTable(m)}
                        />
                      </div>
                    );
                  } else if (REGRESSORS.has(m)) {
                    const vals = rows.map(r => r.prediction).filter(x => typeof x === 'number');
                    return (
                      <div key={m} id={`model-${m}`} className="scroll-mt-20 bg-gradient-to-br from-white to-emerald-50 border border-emerald-200 rounded-2xl p-6 hover:shadow-lg transition-all duration-200">
                        <div className="flex items-center gap-3 mb-4">
                          <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
                            <BarChart3 className="w-5 h-5 text-white" />
                          </div>
                          <h3 className="text-xl font-bold text-gray-800">{m}</h3>
                          <span className="text-sm bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full font-semibold">regression</span>
                        </div>
                        <RegressorHistogram values={vals} title={`${m} — Prediction Distribution`} />
                      </div>
                    );
                  }
                  return null;
                })}
              </div>
            </div>
          </div>
        )}

        {anom && (
          <div id="anomalies-section" className="scroll-mt-20 bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl">
                <AlertTriangle className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800">Anomalies</h2>
            </div>
            <pre className="text-sm bg-gradient-to-r from-gray-50 to-orange-50 border border-gray-200 rounded-2xl p-4 overflow-auto font-mono">
              {JSON.stringify(anom.summary || anom, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}