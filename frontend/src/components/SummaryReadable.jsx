import React, { useState } from 'react';
import { ChevronDown, ChevronUp, BarChart3, Target, AlertTriangle, Settings } from 'lucide-react';

function KV({ label, value }) {
  return (
    <div className="flex items-start justify-between gap-4 py-2 border-b border-purple-100/50 last:border-0">
      <div className="text-gray-600 font-medium">{label}</div>
      <div className="font-semibold text-gray-800 text-right bg-gradient-to-r from-violet-50 to-purple-50 px-3 py-1 rounded-lg border border-violet-100">
        {String(value ?? '-')}
      </div>
    </div>
  );
}

function CollapsibleSection({ title, children, defaultOpen = false }) {
  const [isOpen, setIsOpen] = useState(defaultOpen);
  
  return (
    <div className="space-y-4">
      <button 
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center justify-between w-full text-left p-4 bg-gradient-to-r from-white to-gray-50 rounded-xl border border-gray-200 hover:border-violet-300 transition-all duration-200 group"
      >
        <span className="text-lg font-semibold text-gray-800 group-hover:text-violet-700 transition-colors">
          {title}
        </span>
        <div className="p-1 rounded-lg bg-gray-100 group-hover:bg-violet-100 transition-colors">
          {isOpen ? (
            <ChevronUp className="w-5 h-5 text-gray-600 group-hover:text-violet-600 transition-colors" />
          ) : (
            <ChevronDown className="w-5 h-5 text-gray-600 group-hover:text-violet-600 transition-colors" />
          )}
        </div>
      </button>
      {isOpen && (
        <div className="bg-gradient-to-br from-white to-violet-50 border border-violet-200 rounded-2xl p-6 shadow-sm">
          {children}
        </div>
      )}
    </div>
  );
}

export default function SummaryReadable({ summary }) {
  if (!summary) return null;

  const risk = summary.risk || {};
  const anomaly = summary.anomaly || {};
  const counts = risk.counts || {};
  const selectedModels = risk.selected_models || [];

  // Separate classifiers and regressors
  const classifiers = [];
  const regressors = [];

  Object.entries(counts).forEach(([modelName, data]) => {
    if (data.positives !== undefined && data.total !== undefined) {
      const positiveRate = ((data.positives / data.total) * 100).toFixed(1);
      classifiers.push({
        name: modelName,
        positives: data.positives,
        total: data.total,
        rate: positiveRate
      });
    } else if (data.n !== undefined && data.mean_prediction !== undefined) {
      regressors.push({
        name: modelName,
        n: data.n,
        mean: data.mean_prediction.toFixed(3)
      });
    }
  });

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
      <CollapsibleSection title="Analysis Summary" defaultOpen={false}>
        <div className="space-y-8">
          {/* Overview */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl">
                <Target className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                Overview
              </h3>
            </div>
            <div className="grid sm:grid-cols-3 gap-4">
              <div className="bg-gradient-to-br from-white to-blue-50 border border-blue-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
                <KV label="Dataset ID" value={risk.dataset_id} />
              </div>
              <div className="bg-gradient-to-br from-white to-blue-50 border border-blue-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
                <KV label="Strategy ID" value={risk.strategy_id} />
              </div>
              <div className="bg-gradient-to-br from-white to-blue-50 border border-blue-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
                <KV label="Total Models" value={selectedModels.length} />
              </div>
            </div>
          </div>

          {/* Model Types */}
          <div>
            <div className="flex items-center gap-3 mb-4">
              <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl">
                <Settings className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-lg font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                Model Types
              </h3>
            </div>
            <div className="flex flex-wrap items-center gap-3">
              <div className="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold bg-gradient-to-r from-violet-100 to-purple-100 text-violet-700 border border-violet-200 shadow-sm">
                {classifiers.length} Classifiers
              </div>
              <div className="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-700 border border-emerald-200 shadow-sm">
                {regressors.length} Regressors
              </div>
            </div>
          </div>

          {/* Classification Results */}
          {classifiers.length > 0 && (
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl">
                  <BarChart3 className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-bold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">
                  Classification Results
                </h3>
              </div>
              <div className="space-y-4 max-h-80 overflow-y-auto">
                {classifiers.map(model => (
                  <div key={model.name} className="bg-gradient-to-br from-white to-violet-50 border border-violet-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
                    <div className="flex items-center justify-between mb-3">
                      <div className="font-semibold text-gray-800">{model.name}</div>
                      <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-gradient-to-r from-red-100 to-orange-100 text-red-700 border border-red-200">
                        {model.rate}% positive
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-white/80 border border-violet-100 rounded-lg p-3">
                        <KV label="Positives" value={model.positives.toLocaleString()} />
                      </div>
                      <div className="bg-white/80 border border-violet-100 rounded-lg p-3">
                        <KV label="Total" value={model.total.toLocaleString()} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Regression Results */}
          {regressors.length > 0 && (
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
                  <BarChart3 className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                  Regression Results
                </h3>
              </div>
              <div className="space-y-4">
                {regressors.map(model => (
                  <div key={model.name} className="bg-gradient-to-br from-white to-emerald-50 border border-emerald-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
                    <div className="flex items-center justify-between mb-3">
                      <div className="font-semibold text-gray-800">{model.name}</div>
                      <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 border border-blue-200">
                        μ = {model.mean}
                      </div>
                    </div>
                    <div className="bg-white/80 border border-emerald-100 rounded-lg p-3">
                      <KV label="Samples" value={model.n.toLocaleString()} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Anomaly Detection */}
          {anomaly.n_anomalies !== undefined && (
            <div>
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl">
                  <AlertTriangle className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                  Anomaly Detection
                </h3>
              </div>
              <div className="bg-gradient-to-br from-white to-orange-50 border border-orange-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
                <div className="flex items-center justify-between mb-3">
                  <div className="font-semibold text-orange-800">Anomalies Detected</div>
                  <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-gradient-to-r from-orange-100 to-red-100 text-orange-700 border border-orange-200">
                    {((anomaly.n_anomalies / anomaly.total) * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white/80 border border-orange-100 rounded-lg p-3">
                    <KV label="Anomalies" value={anomaly.n_anomalies.toLocaleString()} />
                  </div>
                  <div className="bg-white/80 border border-orange-100 rounded-lg p-3">
                    <KV label="Total" value={anomaly.total.toLocaleString()} />
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </CollapsibleSection>
    </div>
  );
}