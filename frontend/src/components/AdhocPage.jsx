import React, { useState } from 'react';
import { Brain, User, Dice3, X, Eye, EyeOff, ChevronDown, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { api } from '../api';

// Import the actual ModelOutputs component
import ModelOutputs from './ModelOutputs';

export default function AdhocPage() {
  const [datasetId, setDatasetId] = useState('');
  const [strategyId, setStrategyId] = useState('');
  const [patient, setPatient] = useState({});
  const [res, setRes] = useState(null);
  const [note, setNote] = useState('');
  const [showInputs, setShowInputs] = useState(true);
  const [loading, setLoading] = useState(false);

  async function loadSample() {
    setNote('');
    setRes(null);
    setShowInputs(true);
    setLoading(true);
    try {
      const client = api();
      const r = await client.get('/analytics/adhoc/random', { params: { dataset_id: Number(datasetId) }});
      setPatient(r.data?.patient || {});
    } catch (e) {
      setNote('Failed to load a sample patient.');
    } finally {
      setLoading(false);
    }
  }

  async function predict() {
    setNote(''); 
    setRes(null);
    setLoading(true);
    try {
      const client = api();
      const payload = { dataset_id: Number(datasetId), patient };
      if (strategyId) payload.strategy_id = Number(strategyId);
      const r = await client.post('/analytics/adhoc/predict', payload);
      setRes(r.data || r);
      setShowInputs(false);
    } catch (e) {
      setNote('Prediction failed.');
    } finally {
      setLoading(false);
    }
  }

  function onFieldChange(k, v) {
    setPatient(p => ({ ...p, [k]: v }));
  }

  const hasPatientData = Object.keys(patient).length > 0;
  const isError = note.includes('failed') || note.includes('Failed');

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl shadow-lg">
              <Brain className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              Ad-hoc Prediction
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Generate real-time predictions for individual patients</p>
        </div>

        <div className="space-y-8">
          {/* Configuration Section */}
          <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
                <User className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800">Configuration</h2>
            </div>

            <div className="grid md:grid-cols-3 gap-6 mb-6">
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
              <div className="space-y-3">
                <label className="block text-sm font-semibold text-gray-700 opacity-0">Actions</label>
                <div className="flex gap-3">
                  <button 
                    className={`flex items-center gap-2 px-4 py-3 rounded-xl font-semibold transition-all duration-200 flex-1 ${
                      loading || !datasetId 
                        ? 'bg-gray-400 text-white cursor-not-allowed' 
                        : 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white hover:from-blue-600 hover:to-cyan-600 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                    }`}
                    onClick={loadSample} 
                    disabled={loading || !datasetId}
                  >
                    {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Dice3 className="w-4 h-4" />}
                    Load Sample
                  </button>
                  <button 
                    className="flex items-center gap-2 px-4 py-3 rounded-xl font-semibold bg-gray-200 text-gray-700 hover:bg-gray-300 transition-all duration-200"
                    onClick={() => {setPatient({}); setRes(null); setShowInputs(true); setNote('');}}
                  >
                    <X className="w-4 h-4" />
                    Clear
                  </button>
                </div>
              </div>
            </div>

            {note && (
              <div className={`p-4 rounded-2xl flex items-center gap-3 ${
                isError 
                  ? 'bg-red-50 border border-red-200 text-red-700' 
                  : 'bg-blue-50 border border-blue-200 text-blue-700'
              }`}>
                {isError ? (
                  <AlertCircle className="w-5 h-5 text-red-500" />
                ) : (
                  <CheckCircle className="w-5 h-5 text-blue-500" />
                )}
                <span className="text-sm font-medium">{note}</span>
              </div>
            )}
          </div>

          {/* Patient Data Section */}
          {hasPatientData && (
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
              <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl">
                    <User className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-800">Patient Data</h2>
                    <p className="text-gray-600">Inputs ({Object.keys(patient).length} fields)</p>
                  </div>
                </div>
                <button
                  className="flex items-center gap-2 px-4 py-2 text-sm border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 font-medium"
                  onClick={() => setShowInputs(!showInputs)}
                >
                  {showInputs ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  {showInputs ? 'Hide' : 'Show'} Inputs
                  <ChevronDown className={`w-4 h-4 transition-transform duration-200 ${showInputs ? 'rotate-180' : ''}`} />
                </button>
              </div>
              
              {showInputs && (
                <div className="space-y-6">
                  <div className="grid md:grid-cols-3 gap-4">
                    {Object.entries(patient).map(([k, v]) => (
                      <div key={k} className="space-y-2">
                        <label className="block text-sm font-semibold text-gray-700 capitalize">{k.replace(/_/g, ' ')}</label>
                        <input 
                          className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-violet-400 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80"
                          value={v ?? ''} 
                          onChange={e => onFieldChange(k, e.target.value)}
                          placeholder={`Enter ${k.replace(/_/g, ' ')}...`}
                        />
                      </div>
                    ))}
                  </div>
                  <button 
                    className={`w-full py-4 px-6 rounded-2xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 ${
                      loading 
                        ? 'bg-gray-400 cursor-not-allowed' 
                        : 'bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                    }`}
                    onClick={predict}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        Predicting...
                      </>
                    ) : (
                      <>
                        <Brain className="w-5 h-5" />
                        Predict
                      </>
                    )}
                  </button>
                </div>
              )}
              
              {!showInputs && (
                <div className="flex items-center justify-between">
                  <div className="text-gray-600">
                    Data loaded with {Object.keys(patient).length} input fields
                  </div>
                  <button 
                    className={`py-3 px-6 rounded-2xl font-semibold text-white transition-all duration-200 flex items-center gap-2 ${
                      loading 
                        ? 'bg-gray-400 cursor-not-allowed' 
                        : 'bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
                    }`}
                    onClick={predict}
                    disabled={loading}
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin" />
                        Predicting...
                      </>
                    ) : (
                      <>
                        <Brain className="w-5 h-5" />
                        Predict
                      </>
                    )}
                  </button>
                </div>
              )}
            </div>
          )}

          {/* Results Section */}
          {res && (
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-6">
                <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl">
                  <CheckCircle className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800">Predictions</h2>
              </div>
              <div className="bg-gradient-to-r from-gray-50 to-blue-50 border border-gray-200 rounded-2xl p-6">
                <ModelOutputs result={res.predictions} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}