import React, { useState, useEffect } from 'react';
import { Database, Target, BarChart3, FileText, Search, Brain, Menu, X, User } from 'lucide-react';
import TopBar from './components/TopBar';
import DatasetPage from './components/DatasetPage';
import StrategyPage from './components/StrategyPage';
import AnalysisPage from './components/AnalysisPage';
import ReportsPage from './components/ReportsPage';
import PatientSearchPage from './components/PatientSearchPage';
import AdhocPage from './components/AdhocPage';
import LoginPage from './components/AuthPage';
import SignupPage from './components/AuthPage';
import ProfilePage from './components/ProfilePage';
import { me } from './api';

const tabs = [
  { key: 'datasets', label: 'Datasets', icon: Database, color: 'from-blue-500 to-cyan-500' },
  { key: 'strategy', label: 'Strategy', icon: Target, color: 'from-violet-500 to-purple-500' },
  { key: 'analysis', label: 'Analysis', icon: BarChart3, color: 'from-indigo-500 to-blue-500' },
  { key: 'reports', label: 'Reports', icon: FileText, color: 'from-emerald-500 to-teal-500' },
  { key: 'search', label: 'Patient Search', icon: Search, color: 'from-orange-500 to-red-500' },
  { key: 'adhoc', label: 'Ad-hoc Predictor', icon: Brain, color: 'from-pink-500 to-rose-500' },
];

export default function App() {
  const [tab, setTab] = useState(() => {
    // Check if user is authenticated on initial load
    const isAuthenticated = !!localStorage.getItem('access_token');
    if (!isAuthenticated) {
      return 'login';
    }
    // If authenticated, check for saved tab or default to strategy
    const saved = localStorage.getItem('activeTab');
    return (saved && tabs.some(t => t.key === saved)) ? saved : 'strategy';
  });
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [auth, setAuth] = useState(!!localStorage.getItem('access_token'));

  useEffect(() => {
    // Only save tab if it's not login/signup
    if (tab !== 'login' && tab !== 'signup') {
      localStorage.setItem('activeTab', tab);
    }
  }, [tab]);

  useEffect(() => {
    const onMsg = (e) => {
      if (e?.data?.access_token) {
        localStorage.setItem('access_token', e.data.access_token);
        setAuth(true);
        setTab('profile'); // nudge Google users to set password/name
      }
    };
    window.addEventListener('message', onMsg);
    return () => window.removeEventListener('message', onMsg);
  }, []);

  useEffect(() => {
    // same-tab Google callback fallback: #access_token=...
    const hash = window.location.hash || '';
    const m = hash.match(/access_token=([^&]+)/);
    if (m && m[1]) {
      localStorage.setItem('access_token', decodeURIComponent(m[1]));
      setAuth(true);
      setTab('profile');
      // clean hash
      history.replaceState(null, '', window.location.pathname + window.location.search);
    }
  }, []);

  // Redirect to login if not authenticated and trying to access protected pages
  useEffect(() => {
   if (!auth && tab !== 'login' && tab !== 'signup') {
  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100">
      <LoginPage 
        onAuthed={(targetTab) => {
          setAuth(true);
          setTab(targetTab || 'strategy');
        }} 
        switchToSignup={() => setTab('signup')} 
      />
    </div>
  );
}
  }, [auth, tab]);

  const handleTabChange = (key) => {
    setTab(key);
    setMobileMenuOpen(false);
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('activeTab');
    setAuth(false);
    setTab('login');
  };

  const activeTab = tabs.find(t => t.key === tab);

  // Auth flow: if not authenticated, show login/signup
  if (!auth && tab !== 'login' && tab !== 'signup') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100">
        <LoginPage 
          onAuthed={() => setAuth(true)} 
          switchToSignup={() => setTab('signup')} 
        />
      </div>
    );
  }

  if (tab === 'login') {
  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100">
      <LoginPage 
        onAuthed={(targetTab) => {
          setAuth(true);
          setTab(targetTab || 'strategy');
        }} 
        switchToSignup={() => setTab('signup')} 
      />
    </div>
  );
}

// 3. When tab is 'signup'
if (tab === 'signup') {
  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100">
      <SignupPage 
        onAuthed={(targetTab) => {
          setAuth(true);
          setTab(targetTab || 'strategy');
        }} 
        switchToLogin={() => setTab('login')} 
      />
    </div>
  );
}

  if (tab === 'profile') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100">
        <TopBar setTab={setTab} authed={auth} onLogout={handleLogout} />
        
        {/* Add the same navigation bar as other pages */}
        <div className="sticky top-0 z-20 bg-white/90 backdrop-blur-sm border-b border-purple-200 shadow-lg">
          <div className="max-w-7xl mx-auto px-4 py-4">
            {/* Desktop Navigation */}
            <div className="hidden lg:flex gap-3 flex-wrap">
              {tabs.map(t => {
                const Icon = t.icon;
                const isActive = tab === t.key;
                
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
              {/* Add Profile button */}
              <button
                onClick={() => setTab('profile')}
                className="flex items-center gap-2 px-4 py-3 rounded-xl font-semibold transition-all duration-200 transform bg-gradient-to-r from-gray-700 to-gray-900 text-white shadow-lg scale-105 hover:scale-110"
              >
                <User className="w-5 h-5" />
                <span className="hidden xl:inline">Profile</span>
              </button>
            </div>

            {/* Mobile Navigation Toggle */}
            <div className="lg:hidden flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-gradient-to-r from-gray-700 to-gray-900 rounded-xl">
                  <User className="w-5 h-5 text-white" />
                </div>
                <div>
                  <div className="font-semibold text-gray-800">Profile</div>
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
                    const isActive = tab === t.key;
                    
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
                  <button
                    onClick={() => setTab('profile')}
                    className="flex items-center gap-3 px-4 py-3 rounded-xl font-semibold transition-all duration-200 w-full text-left bg-gradient-to-r from-gray-700 to-gray-900 text-white shadow-lg"
                  >
                    <User className="w-5 h-5" />
                    <span>Profile</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
        
        <div className="max-w-7xl mx-auto px-4 py-6">
          <ProfilePage />
        </div>
      </div>
    );
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-purple-50 to-indigo-100">
      <TopBar setTab={setTab} authed={auth} onLogout={handleLogout} />
      
      {/* Enhanced Navigation */}
      <div className="sticky top-0 z-20 bg-white/90 backdrop-blur-sm border-b border-purple-200 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-4">
          {/* Desktop Navigation */}
          <div className="hidden lg:flex gap-3 flex-wrap">
            {tabs.map(t => {
              const Icon = t.icon;
              const isActive = tab === t.key;
              
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
                  const isActive = tab === t.key;
                  
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
          {tab === 'datasets' && <DatasetPage />}
          {tab === 'strategy' && <StrategyPage />}
          {tab === 'analysis' && <AnalysisPage />}
          {tab === 'reports' && <ReportsPage />}
          {tab === 'search' && <PatientSearchPage />}
          {tab === 'adhoc' && <AdhocPage />}
        </div>
      </div>
    </div>
  );
}