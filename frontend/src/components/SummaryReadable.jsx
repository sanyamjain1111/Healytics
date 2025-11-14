import React, { useState } from 'react';
import { ChevronDown, ChevronUp, BarChart3, Target, AlertTriangle, Settings, Eye, EyeOff } from 'lucide-react';

function StatCard({ label, value, gradient, border }) {
  return (
    <div className={`bg-gradient-to-br ${gradient} border ${border} rounded-xl p-4 hover:shadow-md transition-all duration-200`}>
      <div className="text-sm text-gray-600 font-medium mb-1">{label}</div>
      <div className="text-2xl font-bold text-gray-800">{String(value ?? '-')}</div>
    </div>
  );
}

export default function SummaryReadable({ summary, isOpen, onToggle, onGraphsToggle, graphsVisible }) {
  if (!summary) return null;

  const risk = summary.risk || {};
  const anomaly = summary.anomaly || {};
  const counts = risk.counts || {};
  const selectedModels = risk.selected_models || [];

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

  const sections = [
    { id: 'overview-section', label: 'Overview', icon: <Target className="w-4 h-4" /> },
    { id: 'models-section', label: 'Models', icon: <Settings className="w-4 h-4" /> },
    ...(classifiers.length > 0 ? [{ id: 'classification-section', label: 'Classification', icon: <BarChart3 className="w-4 h-4" /> }] : []),
    ...(regressors.length > 0 ? [{ id: 'regression-section', label: 'Regression', icon: <BarChart3 className="w-4 h-4" /> }] : []),
    ...(anomaly.n_anomalies !== undefined ? [{ id: 'anomaly-section', label: 'Anomalies', icon: <AlertTriangle className="w-4 h-4" /> }] : [])
  ];

  const handleNavigate = (sectionId) => {
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
      {/* Header with Toggle */}
      <div className="flex items-center justify-between mb-6">
        <button 
          onClick={onToggle}
          className="flex items-center gap-3 text-2xl font-bold text-gray-800 hover:text-violet-700 transition-colors group"
        >
          <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl group-hover:shadow-lg transition-shadow">
            <BarChart3 className="w-6 h-6 text-white" />
          </div>
          <span>Analysis Summary</span>
          <ChevronDown 
            className={`w-6 h-6 text-gray-400 transition-transform duration-200 ${
              isOpen ? 'rotate-180' : 'rotate-0'
            }`}
          />
        </button>

        {isOpen && (
          <button
            onClick={onGraphsToggle}
            className="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-violet-100 to-purple-100 text-violet-700 rounded-xl hover:from-violet-200 hover:to-purple-200 transition-all duration-200 font-medium border border-violet-200 shadow-sm hover:shadow-md"
          >
            {graphsVisible ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            <span>{graphsVisible ? 'Hide' : 'Show'} Graphs</span>
          </button>
        )}
      </div>

      {isOpen && (
        <div className="space-y-8">
          {/* Overview Section */}
          <div id="overview-section" className="scroll-mt-4">
            <div className="flex items-center gap-3 mb-4 pb-2 border-b-2 border-blue-200">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl">
                <Target className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                Overview
              </h3>
            </div>
            <div className="grid sm:grid-cols-3 gap-4">
              <StatCard 
                label="Dataset ID" 
                value={risk.dataset_id} 
                gradient="from-white to-blue-50"
                border="border-blue-200"
              />
              <StatCard 
                label="Strategy ID" 
                value={risk.strategy_id || 'Auto'} 
                gradient="from-white to-blue-50"
                border="border-blue-200"
              />
              <StatCard 
                label="Total Models" 
                value={selectedModels.length} 
                gradient="from-white to-blue-50"
                border="border-blue-200"
              />
            </div>
          </div>

          {/* Model Types Section */}
          <div id="models-section" className="scroll-mt-4">
            <div className="flex items-center gap-3 mb-4 pb-2 border-b-2 border-indigo-200">
              <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl">
                <Settings className="w-5 h-5 text-white" />
              </div>
              <h3 className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
                Model Types
              </h3>
            </div>
            <div className="grid sm:grid-cols-2 gap-4">
              <StatCard 
                label="Classifiers" 
                value={classifiers.length} 
                gradient="from-white to-violet-50"
                border="border-violet-200"
              />
              <StatCard 
                label="Regressors" 
                value={regressors.length} 
                gradient="from-white to-emerald-50"
                border="border-emerald-200"
              />
            </div>
          </div>

          {/* Classification Results */}
          {classifiers.length > 0 && (
            <div id="classification-section" className="scroll-mt-4">
              <div className="flex items-center gap-3 mb-4 pb-2 border-b-2 border-violet-200">
                <div className="p-2 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl">
                  <BarChart3 className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-xl font-bold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">
                  Classification Results
                </h3>
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                {classifiers.map(model => (
                  <div key={model.name} className="bg-gradient-to-br from-white to-violet-50 border border-violet-200 rounded-xl p-5 hover:shadow-md transition-all duration-200">
                    <div className="flex items-start justify-between mb-3">
                      <div className="font-semibold text-gray-800 text-sm leading-tight">{model.name}</div>
                      <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-red-100 to-orange-100 text-red-700 border border-red-200 whitespace-nowrap">
                        {model.rate}% positive
                      </div>
                    </div>
                    <div className="grid grid-cols-2 gap-3 mt-4">
                      <div className="bg-white/80 border border-violet-100 rounded-lg p-3">
                        <div className="text-xs text-gray-600 mb-1">Positives</div>
                        <div className="text-lg font-bold text-violet-700">{model.positives.toLocaleString()}</div>
                      </div>
                      <div className="bg-white/80 border border-violet-100 rounded-lg p-3">
                        <div className="text-xs text-gray-600 mb-1">Total</div>
                        <div className="text-lg font-bold text-gray-700">{model.total.toLocaleString()}</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Regression Results */}
          {regressors.length > 0 && (
            <div id="regression-section" className="scroll-mt-4">
              <div className="flex items-center gap-3 mb-4 pb-2 border-b-2 border-emerald-200">
                <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
                  <BarChart3 className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-xl font-bold bg-gradient-to-r from-emerald-600 to-teal-600 bg-clip-text text-transparent">
                  Regression Results
                </h3>
              </div>
              <div className="grid md:grid-cols-2 gap-4">
                {regressors.map(model => (
                  <div key={model.name} className="bg-gradient-to-br from-white to-emerald-50 border border-emerald-200 rounded-xl p-5 hover:shadow-md transition-all duration-200">
                    <div className="flex items-start justify-between mb-3">
                      <div className="font-semibold text-gray-800 text-sm leading-tight">{model.name}</div>
                      <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 border border-blue-200 whitespace-nowrap">
                        μ = {model.mean}
                      </div>
                    </div>
                    <div className="bg-white/80 border border-emerald-100 rounded-lg p-3 mt-4">
                      <div className="text-xs text-gray-600 mb-1">Samples</div>
                      <div className="text-lg font-bold text-emerald-700">{model.n.toLocaleString()}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Anomaly Detection */}
          {anomaly.n_anomalies !== undefined && (
            <div id="anomaly-section" className="scroll-mt-4">
              <div className="flex items-center gap-3 mb-4 pb-2 border-b-2 border-orange-200">
                <div className="p-2 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl">
                  <AlertTriangle className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                  Anomaly Detection
                </h3>
              </div>
              <div className="bg-gradient-to-br from-white to-orange-50 border border-orange-200 rounded-xl p-5 hover:shadow-md transition-all duration-200">
                <div className="flex items-center justify-between mb-4">
                  <div className="font-semibold text-orange-800">Anomalies Detected</div>
                  <div className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-gradient-to-r from-orange-100 to-red-100 text-orange-700 border border-orange-200">
                    {((anomaly.n_anomalies / anomaly.total) * 100).toFixed(1)}%
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white/80 border border-orange-100 rounded-lg p-4">
                    <div className="text-xs text-gray-600 mb-1">Anomalies</div>
                    <div className="text-2xl font-bold text-orange-700">{anomaly.n_anomalies.toLocaleString()}</div>
                  </div>
                  <div className="bg-white/80 border border-orange-100 rounded-lg p-4">
                    <div className="text-xs text-gray-600 mb-1">Total</div>
                    <div className="text-2xl font-bold text-gray-700">{anomaly.total.toLocaleString()}</div>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}