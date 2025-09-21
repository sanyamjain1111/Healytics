import ReportReadable from './ReportReadable';
import React, { useState } from 'react';
import { FileText, BarChart3, Loader2, AlertCircle, CheckCircle } from 'lucide-react';
import { api } from '../api';

export default function ReportsPage() {
  const [datasetId, setDatasetId] = useState('');
  const [res, setRes] = useState(null);
  const [loading, setLoading] = useState(false);
  const [note, setNote] = useState('');

  async function generate() {
    setLoading(true); 
    setNote(''); 
    setRes(null);
    try {
      const client = api();
      const r = await client.post('/reports/generate', { dataset_id: Number(datasetId) });
      setRes(r.data?.report || r.data);
    } catch (e) {
      setNote('Failed to generate report.');
    } finally {
      setLoading(false);
    }
  }

  const isError = note.includes('failed') || note.includes('Failed');

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl shadow-lg">
              <FileText className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              Report Generator
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Generate comprehensive analytics reports from your datasets</p>
        </div>

        {/* Input Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 mb-8 hover:shadow-2xl transition-all duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Generate Report</h2>
          </div>

          <div className="grid md:grid-cols-3 gap-6 items-end">
            <div className="md:col-span-2 space-y-3">
              <label className="block text-sm font-semibold text-gray-700">Dataset ID</label>
              <input 
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-violet-400 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80"
                value={datasetId} 
                onChange={e => setDatasetId(e.target.value)}
                placeholder="Enter dataset ID to generate report..."
              />
            </div>
            
            <button 
              className={`w-full py-4 px-6 rounded-2xl font-semibold text-white transition-all duration-200 flex items-center justify-center gap-2 ${
                loading || !datasetId 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-gradient-to-r from-violet-600 to-purple-600 hover:from-violet-700 hover:to-purple-700 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
              }`}
              onClick={generate} 
              disabled={loading || !datasetId}
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <FileText className="w-5 h-5" />
                  Generate Report
                </>
              )}
            </button>
          </div>

          {note && (
            <div className={`mt-6 p-4 rounded-2xl flex items-center gap-3 ${
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

        {/* Report Results */}
        {res && (
          <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl">
                <CheckCircle className="w-6 h-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-800">Generated Report</h2>
            </div>
            <ReportReadable report={res} />
          </div>
        )}
      </div>
    </div>
  );
}