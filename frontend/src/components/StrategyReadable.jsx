import React, { useRef, useEffect } from 'react';
import { Target, Brain, Settings, CheckCircle, Eye, BarChart3 } from 'lucide-react';

function KV({ label, value }) {
  return (
    <div className="flex items-start justify-between gap-4 py-3 border-b border-purple-100/50">
      <div className="text-gray-600 font-medium">{label}</div>
      <div className="font-semibold text-gray-800 text-right bg-gradient-to-r from-violet-50 to-purple-50 px-3 py-1 rounded-lg border border-violet-100">
        {String(value ?? '-')}
      </div>
    </div>
  );
}

export default function StrategyReadable({ strategy, sectionRefs }) {
  if (!strategy) return null;
  const s = strategy;
  const thresholds = s.thresholds || {};
  const preprocessing = s.preprocessing || {};
  const metrics = (s.validation_plan?.metrics) || {};
  const llm = s.llm_models_block || [];

  // Create refs for each section
  const overviewRef = useRef(null);
  const selectedModelsRef = useRef(null);
  const thresholdsRef = useRef(null);
  const preprocessingRef = useRef(null);
  const validationRef = useRef(null);
  const visualizationRef = useRef(null);
  const llmModelsRef = useRef(null);

  // Pass refs back to parent component
  useEffect(() => {
    if (sectionRefs) {
      sectionRefs.current = {
        overview: overviewRef,
        selected_models: selectedModelsRef,
        thresholds: thresholdsRef,
        preprocessing: preprocessingRef,
        validation_plan: validationRef,
        visualization_specifications: visualizationRef,
        llm_models_block: llmModelsRef
      };
    }
  }, [sectionRefs]);

  return (
    <div className="space-y-8">
      {/* Overview Section */}
      <div id="section-overview" ref={overviewRef} className="scroll-mt-24">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl shadow-md">
            <Target className="w-5 h-5 text-white" />
          </div>
          <h3 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
            Overview
          </h3>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold bg-gradient-to-r from-violet-100 to-purple-100 text-violet-700 border border-violet-200 shadow-sm hover:shadow-md transition-shadow">
            Version: {s.version || '-'}
          </span>
          <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-700 border border-emerald-200 shadow-sm hover:shadow-md transition-shadow">
            {(s.selected_models || []).length} models
          </span>
          <span className="inline-flex items-center px-4 py-2 rounded-full text-sm font-semibold bg-gradient-to-r from-orange-100 to-red-100 text-orange-700 border border-orange-200 shadow-sm hover:shadow-md transition-shadow">
            {Object.keys(thresholds).length} thresholds
          </span>
        </div>
      </div>

      {/* Selected Models Section */}
      {(s.selected_models || []).length > 0 && (
        <div id="section-selected_models" ref={selectedModelsRef} className="scroll-mt-24">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl shadow-md">
              <Brain className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              Selected Models
            </h3>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {s.selected_models.map(m => (
              <div key={m} className="group bg-gradient-to-br from-white to-indigo-50 border border-indigo-200 rounded-xl p-4 hover:shadow-lg transition-all duration-200 hover:-translate-y-1 hover:border-indigo-300">
                <span className="font-semibold text-gray-800 group-hover:text-indigo-700 transition-colors">
                  {m}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Thresholds Section */}
      {Object.keys(thresholds).length > 0 && (
        <div id="section-thresholds" ref={thresholdsRef} className="scroll-mt-24">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-pink-500 to-rose-500 rounded-xl shadow-md">
              <Settings className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-pink-600 to-rose-600 bg-clip-text text-transparent">
              Thresholds
            </h3>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(thresholds).map(([k, v]) => (
              <div key={k} className="group bg-gradient-to-br from-white to-pink-50 border border-pink-200 rounded-xl p-4 hover:shadow-lg transition-all duration-200 hover:-translate-y-1">
                <div className="flex items-center justify-between">
                  <div className="text-gray-700 font-medium group-hover:text-pink-700 transition-colors">
                    {k}
                  </div>
                  <div className="bg-gradient-to-r from-pink-500 to-rose-500 text-white px-3 py-1 rounded-full text-sm font-semibold shadow-sm">
                    {v}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Preprocessing Section */}
      <div id="section-preprocessing" ref={preprocessingRef} className="scroll-mt-24">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-gradient-to-r from-teal-500 to-cyan-500 rounded-xl shadow-md">
            <Settings className="w-5 h-5 text-white" />
          </div>
          <h3 className="text-xl font-bold bg-gradient-to-r from-teal-600 to-cyan-600 bg-clip-text text-transparent">
            Preprocessing
          </h3>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          {preprocessing.imputation && (
            <div className="bg-gradient-to-br from-white to-teal-50 border border-teal-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
              <KV label="Imputation" value={preprocessing.imputation} />
            </div>
          )}
          {preprocessing.outliers && (
            <div className="bg-gradient-to-br from-white to-teal-50 border border-teal-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
              <KV label="Outliers" value={preprocessing.outliers} />
            </div>
          )}
          {preprocessing.encoding && (
            <div className="bg-gradient-to-br from-white to-teal-50 border border-teal-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
              <KV label="Encoding" value={preprocessing.encoding} />
            </div>
          )}
          {preprocessing.scaling && (
            <div className="bg-gradient-to-br from-white to-teal-50 border border-teal-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
              <KV label="Scaling" value={preprocessing.scaling} />
            </div>
          )}
        </div>
      </div>

      {/* Validation Section */}
      <div id="section-validation_plan" ref={validationRef} className="scroll-mt-24">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-gradient-to-r from-amber-500 to-orange-500 rounded-xl shadow-md">
            <CheckCircle className="w-5 h-5 text-white" />
          </div>
          <h3 className="text-xl font-bold bg-gradient-to-r from-amber-600 to-orange-600 bg-clip-text text-transparent">
            Validation
          </h3>
        </div>
        <div className="grid sm:grid-cols-2 gap-4">
          <div className="bg-gradient-to-br from-white to-amber-50 border border-amber-200 rounded-xl p-4 hover:shadow-md transition-all duration-200">
            <KV label="CV Folds" value={s.validation_plan?.cv_folds ?? '-'} />
          </div>
          <div className="bg-gradient-to-br from-white to-amber-50 border border-amber-200 rounded-xl p-4 space-y-4 hover:shadow-md transition-all duration-200">
            <div>
              <div className="text-gray-600 font-semibold mb-2">Classification Metrics</div>
              <div className="flex flex-wrap gap-2">
                {(metrics.classification || []).map(m => (
                  <span key={m} className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-700 border border-blue-200">
                    {m}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <div className="text-gray-600 font-semibold mb-2">Regression Metrics</div>
              <div className="flex flex-wrap gap-2">
                {(metrics.regression || []).map(m => (
                  <span key={m} className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 border border-green-200">
                    {m}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Visualization Section */}
      {s.visualization_specifications && (
        <div id="section-visualization_specifications" ref={visualizationRef} className="scroll-mt-24">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl shadow-md">
              <Eye className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              Visualization Specs
            </h3>
          </div>
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {Object.entries(s.visualization_specifications).map(([k, v]) => (
              <div key={k} className="bg-gradient-to-br from-white to-purple-50 border border-purple-200 rounded-xl p-4 hover:shadow-lg transition-all duration-200 hover:-translate-y-1">
                <div className="font-semibold text-gray-800 mb-3 text-lg">{k}</div>
                <pre className="text-xs text-gray-600 bg-gradient-to-r from-gray-50 to-purple-50 p-3 rounded-lg overflow-x-auto border border-gray-200 font-mono">
                  {JSON.stringify(v, null, 2)}
                </pre>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Model Block Section */}
      {llm.length > 0 && (
        <div id="section-llm_models_block" ref={llmModelsRef} className="scroll-mt-24">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl shadow-md">
              <BarChart3 className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-xl font-bold bg-gradient-to-r from-violet-600 to-purple-600 bg-clip-text text-transparent">
              Model Block
            </h3>
          </div>
          <div className="space-y-6">
            {llm.map((m, i) => (
              <div key={i} className="group bg-gradient-to-br from-white to-violet-50 border border-violet-200 rounded-2xl p-6 hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
                <div className="flex items-center justify-between flex-wrap gap-3 mb-4">
                  <div className="font-bold text-xl text-gray-800 group-hover:text-violet-700 transition-colors">
                    {m.model_name}
                  </div>
                  <div className="flex items-center gap-3">
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-700 border border-blue-200 shadow-sm">
                      {m.task_type}
                    </span>
                    <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 border border-green-200 shadow-sm">
                      Priority: {m.priority}
                    </span>
                  </div>
                </div>
                {m.target_signal_candidates?.length > 0 && (
                  <div className="mb-4">
                    <div className="text-gray-600 font-semibold mb-3">Target Signals</div>
                    <div className="flex flex-wrap gap-2">
                      {m.target_signal_candidates.map(t => (
                        <span key={t} className="inline-flex items-center px-3 py-2 rounded-lg text-sm font-semibold bg-gradient-to-r from-amber-100 to-orange-100 text-amber-700 border border-amber-200 shadow-sm hover:shadow-md transition-shadow">
                          {t}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
                {m.rationale && (
                  <div className="bg-gradient-to-r from-gray-50 to-violet-50 border border-gray-200 rounded-xl p-4 shadow-inner">
                    <div className="text-gray-700 leading-relaxed">
                      {m.rationale}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}