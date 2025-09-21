import React, { useState, useEffect } from 'react';
import { Database, Target, BarChart3, FileText, Search, Brain, Menu, X } from 'lucide-react';
import TopBar from './components/TopBar';
import DatasetPage from './components/DatasetPage';
import StrategyPage from './components/StrategyPage';
import AnalysisPage from './components/AnalysisPage';
import ReportsPage from './components/ReportsPage';
import PatientSearchPage from './components/PatientSearchPage';
import AdhocPage from './components/AdhocPage';

const tabs = [
  { key: 'datasets', label: 'Datasets', icon: Database, color: 'from-blue-500 to-cyan-500' },
  { key: 'strategy', label: 'Strategy', icon: Target, color: 'from-violet-500 to-purple-500' },
  { key: 'analysis', label: 'Analysis', icon: BarChart3, color: 'from-indigo-500 to-blue-500' },
  { key: 'reports', label: 'Reports', icon: FileText, color: 'from-emerald-500 to-teal-500' },
  { key: 'search', label: 'Patient Search', icon: Search, color: 'from-orange-500 to-red-500' },
  { key: 'adhoc', label: 'Ad-hoc Predictor', icon: Brain, color: 'from-pink-500 to-rose-500' },
];

export default function App() {
  const [active, setActive] = useState('datasets');
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('activeTab');
    if (saved && tabs.some(t => t.key === saved)) setActive(saved);
  }, []);

  useEffect(() => {
    localStorage.setItem('activeTab', active);
  }, [active]);

  const handleTabChange = (key) => {
    setActive(key);
    setMobileMenuOpen(false);
  };

  const activeTab = tabs.find(t => t.key === active);

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100">
      <TopBar />
      
      {/* Enhanced Navigation */}
      <div className="sticky top-0 z-20 bg-white/90 backdrop-blur-sm border-b border-purple-200 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4">
          {/* Desktop Navigation */}
          <div className="hidden lg:flex gap-3 flex-wrap">
            {tabs.map(t => {
              const Icon = t.icon;
              const isActive = active === t.key;
              
              return (
                <button
                  key={t.key}
                  onClick={() => handleTabChange(t.key)}
                  className={`flex items-center gap-2 px-4 py-3 rounded-xl font-semibold transition-all duration-200 transform ${
                    isActive
                      ? `bg-gradient-to-r ${t.color} text-white shadow-lg scale-105 hover:scale-110`
                      : 'bg-white/80 text-gray-700 border-2 border-gray-200 hover:bg-gray-50 hover:border-gray-300 hover:shadow-md hover:-translate-y-0.5'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="hidden xl:inline">{t.label}</span>
                  <span className="xl:hidden">{t.label.split(' ')[0]}</span>
                </button>
              );
            })}
          </div>

          {/* Mobile Navigation Toggle */}
          <div className="lg:hidden flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className={`p-2 bg-gradient-to-r ${activeTab?.color} rounded-xl`}>
                {activeTab && <activeTab.icon className="w-5 h-5 text-white" />}
              </div>
              <div>
                <div className="font-semibold text-gray-800">{activeTab?.label}</div>
                <div className="text-sm text-gray-600">Current Section</div>
              </div>
            </div>
            
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-xl bg-white border-2 border-gray-300 hover:bg-gray-50 transition-colors"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Menu */}
          {mobileMenuOpen && (
            <div className="lg:hidden mt-4 bg-white/95 backdrop-blur-sm rounded-2xl border border-gray-200 shadow-xl p-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {tabs.map(t => {
                  const Icon = t.icon;
                  const isActive = active === t.key;
                  
                  return (
                    <button
                      key={t.key}
                      onClick={() => handleTabChange(t.key)}
                      className={`flex items-center gap-3 px-4 py-3 rounded-xl font-semibold transition-all duration-200 w-full text-left ${
                        isActive
                          ? `bg-gradient-to-r ${t.color} text-white shadow-lg`
                          : 'bg-gray-50 text-gray-700 hover:bg-gray-100 border border-gray-200'
                      }`}
                    >
                      <Icon className="w-5 h-5" />
                      <span>{t.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Content - Using your existing components */}
      <div className="max-w-7xl mx-auto px-4 py-6">
        <div className="bg-white/80 backdrop-blur-sm rounded-3xl shadow-xl border border-white/50 p-6 hover:shadow-2xl transition-all duration-300">
          {active === 'datasets' && <DatasetPage />}
          {active === 'strategy' && <StrategyPage />}
          {active === 'analysis' && <AnalysisPage />}
          {active === 'reports' && <ReportsPage />}
          {active === 'search' && <PatientSearchPage />}
          {active === 'adhoc' && <AdhocPage />}
        </div>
      </div>
    </div>
  );
}