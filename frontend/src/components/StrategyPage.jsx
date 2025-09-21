import StrategyReadable from './StrategyReadable';
import React, { useState, useRef } from 'react';
import { Target, Brain, Settings, Loader2, CheckCircle, AlertCircle, Eye, EyeOff, ChevronDown, ChevronRight } from 'lucide-react';
import { api } from '../api';

export default function StrategyPage() {
  const [datasetId, setDatasetId] = useState('');
  const [objective, setObjective] = useState('Clinical risk, operations, and outcomes insights with explainability.');
  const [res, setRes] = useState(null);
  const [note, setNote] = useState('');
  const [loading, setLoading] = useState(false);
  const [showRawText, setShowRawText] = useState(false);
  const [activeSection, setActiveSection] = useState('overview');
  const sectionRefs = useRef({});

  async function generate() {
    setLoading(true);
    setNote('');
    setRes(null);
    try {
      const client = api();
      const payload = { dataset_id: Number(datasetId), objective };
      const r = await client.post('/strategy/generate', payload);
      setRes(r.data?.strategy || r.data);
    } catch (e) {
      console.error('API Error:', e);
      setNote('Failed to generate strategy: ' + (e.message || 'Unknown error'));
    } finally {
      setLoading(false);
    }
  }

  console.log('res', res);

  // Get available sections from parsed strategy
  const getAvailableSections = () => {
    if (!res?.parsed) return [];
    
    const sections = [
      { key: 'overview', label: 'Overview' },
      { key: 'selected_models', label: 'Selected Models', available: res.parsed.selected_models?.length > 0 },
      { key: 'thresholds', label: 'Thresholds', available: Object.keys(res.parsed.thresholds || {}).length > 0 },
      { key: 'preprocessing', label: 'Preprocessing', available: res.parsed.preprocessing },
      { key: 'validation_plan', label: 'Validation', available: res.parsed.validation_plan },
      { key: 'visualization_specifications', label: 'Visualizations', available: res.parsed.visualization_specifications },
      { key: 'llm_models_block', label: 'Model Block', available: res.parsed.llm_models_block?.length > 0 }
    ];
    
    return sections.filter(section => section.available !== false);
  };

  const scrollToSection = (sectionKey) => {
    setActiveSection(sectionKey);
    
    console.log(`Clicking section: ${sectionKey}`);
    
    // Use refs to scroll to sections
    const targetRef = sectionRefs.current[sectionKey];
    if (targetRef && targetRef.current) {
      targetRef.current.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start',
        inline: 'nearest'
      });
    } else {
      // Fallback to getElementById
      setTimeout(() => {
        const element = document.getElementById(`section-${sectionKey}`);
        if (element) {
          element.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start',
            inline: 'nearest'
          });
        } else {
          console.log(`Section not found: section-${sectionKey}`);
        }
      }, 100);
    }
  };

  const isError = note.includes('failed') || note.includes('Failed');
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center items-center gap-3 mb-4">
            <div className="p-3 bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl shadow-lg">
              <Target className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-violet-600 to-indigo-600 bg-clip-text text-transparent">
              Strategy Generator
            </h1>
          </div>
          <p className="text-gray-600 text-lg">Generate intelligent ML strategies based on your datasets</p>
        </div>

        {/* Input Section */}
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 mb-8 hover:shadow-2xl transition-all duration-300">
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
              <Settings className="w-6 h-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-800">Configuration</h2>
          </div>

          <div className="grid md:grid-cols-2 gap-6 mb-6">
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
              <label className="block text-sm font-semibold text-gray-700">Objective</label>
              <input 
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-violet-400 focus:ring-4 focus:ring-violet-100 transition-all duration-200 bg-white/80"
                value={objective} 
                onChange={e => setObjective(e.target.value)}
                placeholder="Describe your objective..."
              />
            </div>
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
                Generating Strategy...
              </>
            ) : (
              <>
                <Brain className="w-5 h-5" />
                Generate Strategy
              </>
            )}
          </button>

          {note && (
            <div className={`mt-4 p-4 rounded-2xl flex items-center gap-3 ${
              isError 
                ? 'bg-red-50 border border-red-200 text-red-700' 
                : 'bg-blue-50 border border-blue-200 text-blue-700'
            }`}>
              {isError ? (
                <AlertCircle className="w-5 h-5 text-red-500" />
              ) : (
                <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
              )}
              <span className="text-sm font-medium">{note}</span>
            </div>
          )}
        </div>

        {res && (
          <div className="space-y-6">
            {/* Strategy Info */}
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
              <div className="flex items-center gap-3 mb-4">
                <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl">
                  <CheckCircle className="w-6 h-6 text-white" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800">Created Strategy</h2>
              </div>
              <div className="flex flex-wrap gap-3">
                <div className="bg-gradient-to-r from-violet-100 to-purple-100 text-violet-700 px-4 py-2 rounded-full font-semibold border border-violet-200">
                  Strategy ID: {res.id}
                </div>
                <div className="bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-700 px-4 py-2 rounded-full font-semibold border border-blue-200">
                  Dataset ID: {res.dataset_id}
                </div>
              </div>
            </div>

            {/* Navigation */}
            <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
              <div className="flex flex-wrap gap-3 mb-6">
                {getAvailableSections().map((section) => (
                  <button
                    key={section.key}
                    onClick={() => scrollToSection(section.key)}
                    className={`px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200 ${
                      activeSection === section.key
                        ? 'bg-gradient-to-r from-violet-600 to-purple-600 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200 hover:shadow-md'
                    }`}
                  >
                    {section.label}
                  </button>
                ))}
              </div>
              
              {/* Raw Text Toggle */}
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setShowRawText(!showRawText)}
                  className="flex items-center gap-2 px-4 py-2 text-sm border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 font-medium"
                >
                  {showRawText ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                  {showRawText ? 'Hide Raw Text' : 'Show Raw Text'}
                  {showRawText ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                </button>
              </div>
            </div>

            {/* Display Raw Text (collapsible) */}
            {showRawText && res.raw_text && (
              <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
                <div className="flex items-center gap-3 mb-4">
                  <div className="p-2 bg-gradient-to-r from-gray-500 to-slate-500 rounded-xl">
                    <Eye className="w-6 h-6 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-800">Raw Text</h2>
                </div>
                <pre className="text-sm bg-gray-50 p-4 rounded-2xl overflow-x-auto whitespace-pre-wrap border-2 border-gray-200 max-h-96 overflow-y-auto font-mono">
                  {res.raw_text}
                </pre>
              </div>
            )}

            {/* Display Parsed Strategy using StrategyReadable */}
            {res.parsed && (
              <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
                <div className="flex items-center gap-3 mb-6">
                  <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl">
                    <Target className="w-6 h-6 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-800">Parsed Strategy</h2>
                </div>
                <StrategyReadable strategy={res.parsed} sectionRefs={sectionRefs} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}