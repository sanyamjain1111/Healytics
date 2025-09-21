import React from 'react';
import { Activity, BarChart3, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';

export default function ModelOutputs({ result }) {
  if (!result) return null;
  
  const entries = Object.entries(result);
  const cls = entries.filter(([_, v]) => v && typeof v === 'object' && ('pred' in v));
  const reg = entries.filter(([_, v]) => v && typeof v === 'object' && ('prediction' in v));

  return (
    <div className="space-y-8">
      {cls.length > 0 && (
        <div>
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-800">Classification Models</h3>
              <p className="text-gray-600 text-sm">{cls.length} risk assessment models</p>
            </div>
          </div>
          
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {cls.map(([name, v]) => {
              const riskLevel = v.score >= 0.8 ? 'high' : v.score >= 0.6 ? 'medium' : v.score >= 0.4 ? 'low' : 'minimal';
              const isHighRisk = v.pred;
              
              return (
                <div 
                  key={name} 
                  className={`bg-gradient-to-br from-white to-violet-50 border-2 rounded-2xl p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 ${
                    isHighRisk ? 'border-red-200 bg-gradient-to-br from-red-50 to-orange-50' : 'border-violet-200'
                  }`}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h4 className="font-bold text-gray-800 text-lg mb-1 leading-tight">{name}</h4>
                      <div className="text-sm text-gray-600">Risk Classification</div>
                    </div>
                    
                    <div className="flex flex-col items-end gap-2">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold flex items-center gap-1 ${
                        isHighRisk 
                          ? 'bg-red-100 text-red-800 border border-red-200' 
                          : 'bg-green-100 text-green-800 border border-green-200'
                      }`}>
                        {isHighRisk ? <AlertTriangle className="w-3 h-3" /> : <CheckCircle className="w-3 h-3" />}
                        {isHighRisk ? 'Positive' : 'Negative'}
                      </span>
                      
                      <span className={`text-xs px-2 py-1 rounded-full font-semibold ${
                        riskLevel === 'high' ? 'bg-red-100 text-red-700' :
                        riskLevel === 'medium' ? 'bg-orange-100 text-orange-700' :
                        riskLevel === 'low' ? 'bg-yellow-100 text-yellow-700' :
                        'bg-green-100 text-green-700'
                      }`}>
                        {riskLevel.toUpperCase()}
                      </span>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-sm font-semibold text-gray-700">Score</span>
                        <span className="text-lg font-bold text-gray-800">{((v.score || 0) * 100).toFixed(1)}%</span>
                      </div>
                      
                      <div className="relative">
                        <div className="h-4 rounded-full bg-gray-200 overflow-hidden shadow-inner">
                          <div
                            className={`h-4 rounded-full transition-all duration-500 ease-out ${
                              isHighRisk 
                                ? 'bg-gradient-to-r from-red-400 via-red-500 to-red-600' 
                                : 'bg-gradient-to-r from-green-400 via-green-500 to-green-600'
                            }`}
                            style={{ 
                              width: `${Math.round((v.score || 0) * 100)}%`,
                              boxShadow: isHighRisk ? '0 0 10px rgba(239, 68, 68, 0.4)' : '0 0 10px rgba(34, 197, 94, 0.4)'
                            }}
                          />
                        </div>
                        
                        {/* Threshold marker */}
                        {v.threshold && (
                          <div 
                            className="absolute top-0 h-4 w-0.5 bg-gray-700"
                            style={{ left: `${v.threshold * 100}%` }}
                          >
                            <div className="absolute -top-1 -left-2 w-4 h-4 transform rotate-45 bg-gray-700"></div>
                          </div>
                        )}
                      </div>
                    </div>

                    {v.threshold && (
                      <div className="bg-gray-50 rounded-xl p-3 border border-gray-200">
                        <div className="flex items-center justify-between">
                          <span className="text-xs font-semibold text-gray-600">Threshold</span>
                          <span className="text-sm font-bold text-gray-800">{v.threshold}</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {reg.length > 0 && (
        <div>
          <div className="flex items-center gap-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h3 className="text-xl font-bold text-gray-800">Regression Models</h3>
              <p className="text-gray-600 text-sm">{reg.length} predictive value models</p>
            </div>
          </div>
          
          <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {reg.map(([name, v]) => (
              <div 
                key={name} 
                className="bg-gradient-to-br from-white to-emerald-50 border-2 border-emerald-200 rounded-2xl p-6 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1"
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex-1">
                    <h4 className="font-bold text-gray-800 text-lg mb-1 leading-tight">{name}</h4>
                    <div className="text-sm text-gray-600">Predictive Value</div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-emerald-600" />
                  </div>
                </div>

                <div className="text-center">
                  <div className="bg-gradient-to-r from-emerald-500 to-teal-500 text-white rounded-2xl p-4 shadow-lg">
                    <div className="text-3xl font-bold mb-1">{Number(v.prediction).toFixed(3)}</div>
                    <div className="text-emerald-100 text-sm font-medium">Predicted Value</div>
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