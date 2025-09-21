import React from 'react';
import { BarChart3, Target, Lightbulb, Settings, TrendingUp, AlertTriangle } from 'lucide-react';

function Stat({ label, value, sub }) {
  return (
    <div className="group bg-gradient-to-br from-white to-indigo-50 border border-indigo-200 rounded-xl p-6 text-center hover:shadow-lg transition-all duration-200 hover:-translate-y-1">
      <div className="text-3xl font-bold text-gray-800 mb-2 group-hover:text-indigo-700 transition-colors">
        {value}
      </div>
      <div className="text-gray-600 font-semibold">{label}</div>
      {sub && (
        <div className="text-xs text-gray-500 mt-2 bg-gray-50 px-2 py-1 rounded-full inline-block">
          {sub}
        </div>
      )}
    </div>
  );
}

export default function ReportReadable({ report }) {
  if (!report) return null;
  const s = report.summary || {};
  const risk = s.risk_overview || {};
  const counts = risk.counts || {};
  const insights = report.insights || {};

  const models = Object.entries(counts).map(([name, obj]) => ({
    model: name,
    positives: obj.positives ?? obj.n ?? 0,
    total: obj.total ?? obj.n ?? 0,
    rate: (obj.positives != null && obj.total) ? (obj.positives / obj.total) : null,
  }));
  const cls = models.filter(m => m.total && m.rate !== null);

  return (
    <div className="space-y-8">
      {/* Stats Overview */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <Stat 
          label="Dataset ID" 
          value={String(report.dataset_id ?? s.dataset_id ?? '-')} 
        />
        <Stat 
          label="Strategy ID" 
          value={String(risk.strategy_id ?? s.strategy_id ?? '-')} 
        />
        <Stat 
          label="Selected Models" 
          value={String((risk.selected_models || []).length)} 
        />
        <Stat 
          label="Anomalies" 
          value={`${s.anomaly_overview?.n_anomalies ?? 0} / ${s.anomaly_overview?.total ?? 0}`} 
          sub="(detected / total)"
        />
      </div>

      {/* Executive Summary */}
      {insights.executive_summary && (
        <div className="bg-gradient-to-br from-white to-blue-50 border border-blue-200 rounded-2xl p-8 hover:shadow-lg transition-all duration-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl">
              <Target className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              Executive Summary
            </h3>
          </div>
          <p className="text-gray-700 leading-relaxed text-lg bg-gradient-to-r from-gray-50 to-blue-50 p-4 rounded-xl border border-gray-200">
            {insights.executive_summary}
          </p>
        </div>
      )}

      {/* Model Positives Table */}
      {cls.length > 0 && (
        <div className="bg-gradient-to-br from-white to-purple-50 border border-purple-200 rounded-2xl p-8 hover:shadow-lg transition-all duration-200">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Model Positives
            </h3>
          </div>
          <div className="overflow-hidden rounded-xl border border-purple-200">
            <table className="min-w-full bg-white">
              <thead className="bg-gradient-to-r from-purple-500 to-pink-500">
                <tr>
                  <th className="py-4 px-6 text-left font-semibold text-white">Model</th>
                  <th className="py-4 px-6 text-left font-semibold text-white">Positives</th>
                  <th className="py-4 px-6 text-left font-semibold text-white">Total</th>
                  <th className="py-4 px-6 text-left font-semibold text-white">Rate</th>
                </tr>
              </thead>
              <tbody>
                {cls.map((m, i) => (
                  <tr key={m.model} className={`hover:bg-purple-50 transition-colors ${i % 2 ? 'bg-gray-50' : 'bg-white'}`}>
                    <td className="py-4 px-6 font-semibold text-gray-800 border-b border-gray-200">
                      {m.model}
                    </td>
                    <td className="py-4 px-6 text-gray-700 border-b border-gray-200">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-green-100 text-green-700">
                        {m.positives}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-gray-700 border-b border-gray-200">
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-blue-100 text-blue-700">
                        {m.total}
                      </span>
                    </td>
                    <td className="py-4 px-6 text-gray-700 border-b border-gray-200">
                      {m.rate != null ? (
                        <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-purple-100 text-purple-700">
                          {(m.rate * 100).toFixed(2)}%
                        </span>
                      ) : (
                        <span className="text-gray-400">-</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Key Findings */}
      {Array.isArray(insights.key_findings) && insights.key_findings.length > 0 && (
        <div className="bg-gradient-to-br from-white to-emerald-50 border border-emerald-200 rounded-2xl p-8 hover:shadow-lg transition-all duration-200">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
              Key Findings
            </h3>
          </div>
          <div className="space-y-4">
            {insights.key_findings.map((finding, i) => (
              <div key={i} className="flex items-start gap-4 bg-gradient-to-r from-emerald-50 to-teal-50 p-4 rounded-xl border border-emerald-200">
                <div className="flex-shrink-0 w-6 h-6 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                  {i + 1}
                </div>
                <p className="text-gray-700 leading-relaxed">{finding}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {Array.isArray(insights.recommendations) && insights.recommendations.length > 0 && (
        <div className="bg-gradient-to-br from-white to-amber-50 border border-amber-200 rounded-2xl p-8 hover:shadow-lg transition-all duration-200">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl">
              <Lightbulb className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">
              Recommendations
            </h3>
          </div>
          <div className="space-y-4">
            {insights.recommendations.map((rec, i) => (
              <div key={i} className="flex items-start gap-4 bg-gradient-to-r from-amber-50 to-orange-50 p-4 rounded-xl border border-amber-200">
                <div className="flex-shrink-0 w-6 h-6 bg-gradient-to-r from-amber-500 to-orange-500 rounded-full flex items-center justify-center text-white text-sm font-bold">
                  {i + 1}
                </div>
                <p className="text-gray-700 leading-relaxed">{rec}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Parameters */}
      {s.params && (
        <div className="bg-gradient-to-br from-white to-indigo-50 border border-indigo-200 rounded-2xl p-8 hover:shadow-lg transition-all duration-200">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl">
              <Settings className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Parameters
            </h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(s.params).map(([k, v]) => (
              <div key={k} className="bg-gradient-to-br from-white to-indigo-50 border border-indigo-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
                <div className="flex items-center justify-between">
                  <div className="text-gray-700 font-medium">{k}</div>
                  <div className="bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-3 py-1 rounded-full text-sm font-semibold">
                    {String(v)}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}