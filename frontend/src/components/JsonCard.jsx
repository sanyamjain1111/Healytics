import React, { useState } from 'react';
import { FileText, Eye, EyeOff, ChevronDown, ChevronRight, Code } from 'lucide-react';

export default function JsonCard({ title, data }) {
  const [open, setOpen] = useState(false);
  
  const dataString = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
  const lineCount = dataString.split('\n').length;
  const charCount = dataString.length;

  return (
    <div className="bg-white/80 backdrop-blur-sm rounded-2xl shadow-lg border border-white/50 p-6 hover:shadow-xl transition-all duration-300">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-r from-slate-500 to-gray-500 rounded-xl">
            <FileText className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-800 text-lg">{title}</h3>
            <div className="text-sm text-gray-500">
              {lineCount} lines • {charCount} characters
            </div>
          </div>
        </div>
        
        <button 
          className="flex items-center gap-2 px-4 py-2 text-sm border-2 border-gray-300 rounded-xl hover:bg-gray-50 hover:border-gray-400 transition-all duration-200 font-medium"
          onClick={() => setOpen(!open)}
        >
          {open ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          {open ? 'Hide' : 'Show'}
          {open ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
        </button>
      </div>
      
      {open && (
        <div className="mt-6 space-y-4">
          <div className="flex items-center gap-2 text-sm text-gray-600 bg-gradient-to-r from-blue-50 to-indigo-50 px-3 py-2 rounded-xl border border-blue-200">
            <Code className="w-4 h-4" />
            <span className="font-medium">JSON Data Preview</span>
          </div>
          
          <div className="bg-gradient-to-br from-gray-900 to-slate-800 rounded-xl border-2 border-gray-300 overflow-hidden shadow-inner">
            <div className="bg-gradient-to-r from-gray-700 to-slate-600 px-4 py-2 border-b border-gray-600">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-3 h-3 rounded-full bg-red-400"></div>
                  <div className="w-3 h-3 rounded-full bg-yellow-400"></div>
                  <div className="w-3 h-3 rounded-full bg-green-400"></div>
                </div>
                <span className="text-gray-300 text-sm font-mono">{title}.json</span>
              </div>
            </div>
            
            <pre className="text-sm overflow-auto max-h-96 p-4 font-mono text-gray-100 leading-relaxed">
              {dataString}
            </pre>
          </div>
          
          <div className="flex items-center gap-4 text-xs text-gray-500 bg-gray-50 px-3 py-2 rounded-lg">
            <span>Size: {(charCount / 1024).toFixed(2)} KB</span>
            <span>•</span>
            <span>Lines: {lineCount}</span>
            <span>•</span>
            <span>Format: JSON</span>
          </div>
        </div>
      )}
    </div>
  );
}