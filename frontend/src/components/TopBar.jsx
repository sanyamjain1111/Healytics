import React, { useState, useEffect } from 'react';
import { Settings, Save, Check } from 'lucide-react';
import { getApiBase, setApiBase } from '../api';

export default function TopBar() {
  const [base, setBase] = useState(getApiBase());
  const [saved, setSaved] = useState(false);

  useEffect(() => { setBase(getApiBase()); }, []);
  
  const save = () => {
    setApiBase(base);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="bg-gradient-to-r from-violet-600 via-purple-600 to-indigo-600 border-b border-purple-300/30 shadow-lg backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo Section */}
          <div className="flex items-center gap-4">
            <div className="relative">
              <div className="text-3xl animate-pulse">🧬</div>
              <div className="absolute -top-1 -right-1 w-2 h-2 bg-emerald-400 rounded-full animate-ping"></div>
            </div>
            <div className="text-2xl font-bold text-white tracking-wide">
              <span className="bg-gradient-to-r from-white to-purple-100 bg-clip-text text-transparent">
                Healytics
              </span>
            </div>
          </div>

          {/* API Configuration Section */}
          <div className="flex items-center gap-4 bg-white/10 backdrop-blur-sm rounded-2xl px-6 py-3 border border-white/20 shadow-inner">
            <div className="flex items-center gap-2">
              <div className="p-1.5 bg-white/20 rounded-lg">
                <Settings className="w-4 h-4 text-white" />
              </div>
              <label className="text-sm font-semibold text-white/90">
                API Base
              </label>
            </div>
            
            <div className="flex items-center gap-3">
              <input 
                className="w-80 px-4 py-2 bg-white/90 border-2 border-white/30 rounded-xl text-gray-800 placeholder-gray-500 focus:border-white focus:ring-4 focus:ring-white/20 transition-all duration-200 font-mono text-sm shadow-inner"
                value={base} 
                onChange={e => setBase(e.target.value)} 
                placeholder="http://127.0.0.1:8000"
              />
              
              <button 
                className={`flex items-center gap-2 px-4 py-2 rounded-xl font-semibold text-sm transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5 ${
                  saved 
                    ? 'bg-emerald-500 text-white' 
                    : 'bg-white text-purple-600 hover:bg-purple-50'
                }`}
                onClick={save}
              >
                {saved ? (
                  <>
                    <Check className="w-4 h-4" />
                    Saved!
                  </>
                ) : (
                  <>
                    <Save className="w-4 h-4" />
                    Save
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}