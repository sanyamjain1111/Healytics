import React from 'react';
import { BarChart, Bar, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer, LabelList } from 'recharts';
import { BarChart3, TrendingUp } from 'lucide-react';

export default function RegressorHistogram({ values=[], title }) {
  if (!values || values.length === 0) return null;
  
  const min = Math.min(...values);
  const max = Math.max(...values);
  const nBins = 20;
  const step = (max - min) / nBins || 1;

  const counts = Array.from({length:nBins}, (_,i)=>({ x: min + (i+0.5)*step, count: 0 }));
  for (const v of values) {
    const idx = Math.max(0, Math.min(nBins-1, Math.floor((v - min) / step)));
    counts[idx].count += 1;
  }
  
  // Create gradient colors from teal to orange
  const data = counts.map((d, i) => {
    const t = i/(nBins-1);
    const r = Math.round(22 + t*(220));
    const g = Math.round(163 - t*(120));
    const b = Math.round(74 - t*(40));
    return { ...d, fill: `rgb(${r},${g},${b})` };
  });

  // Define quartile bands for the legend
  const quartileSize = Math.ceil(nBins / 4);
  const quartiles = [
    { key: 'low', label: 'Low', color: data[0]?.fill || '#16a34a' },
    { key: 'mid-low', label: 'Mid-Low', color: data[quartileSize]?.fill || '#84cc16' },
    { key: 'mid-high', label: 'Mid-High', color: data[2*quartileSize]?.fill || '#f97316' },
    { key: 'high', label: 'High', color: data[3*quartileSize] ? data[3*quartileSize].fill : data[data.length-1]?.fill || '#dc2626' }
  ];

  const total = data.reduce((a,x)=>a+(x.count||0),0) || 1;

  // Calculate counts for each quartile
  const quartileCounts = quartiles.map((q, qIdx) => {
    const startIdx = qIdx * quartileSize;
    const endIdx = Math.min((qIdx + 1) * quartileSize, nBins);
    const count = data.slice(startIdx, endIdx).reduce((sum, d) => sum + d.count, 0);
    return { ...q, count };
  });

  return (
    <div className="bg-gradient-to-br from-white to-emerald-50 border border-emerald-200 rounded-2xl p-6 hover:shadow-lg transition-all duration-200">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-gradient-to-r from-emerald-500 to-teal-500 rounded-xl">
          <BarChart3 className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-xl font-bold text-gray-800">{title}</h3>
      </div>
      
      <div className="w-full">
        {/* Quartile Legend */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
          {quartileCounts.map(q=>{
            const pct = ((q.count/total)*100).toFixed(1);
            return (
              <div key={q.key} className="bg-white border border-gray-200 rounded-xl p-3 hover:shadow-md transition-all duration-200">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-4 h-4 rounded-full" style={{backgroundColor:q.color}} />
                  <div className="text-sm font-semibold text-gray-700">{q.label}</div>
                </div>
                <div className="text-lg font-bold text-gray-800">{q.count}</div>
                <div className="text-xs text-gray-500">({pct}%)</div>
              </div>
            );
          })}
        </div>
        
        {/* Statistics Summary */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
          <div className="bg-white border border-emerald-200 rounded-xl p-3">
            <div className="text-sm text-gray-600 mb-1">Total Samples</div>
            <div className="text-lg font-bold text-gray-800">{values.length.toLocaleString()}</div>
          </div>
          <div className="bg-white border border-emerald-200 rounded-xl p-3">
            <div className="text-sm text-gray-600 mb-1">Min Value</div>
            <div className="text-lg font-bold text-gray-800">{min.toFixed(2)}</div>
          </div>
          <div className="bg-white border border-emerald-200 rounded-xl p-3">
            <div className="text-sm text-gray-600 mb-1">Max Value</div>
            <div className="text-lg font-bold text-gray-800">{max.toFixed(2)}</div>
          </div>
          <div className="bg-white border border-emerald-200 rounded-xl p-3">
            <div className="text-sm text-gray-600 mb-1">Mean</div>
            <div className="text-lg font-bold text-gray-800">
              {(values.reduce((a,b) => a+b, 0) / values.length).toFixed(2)}
            </div>
          </div>
        </div>
        
        {/* Chart */}
        <div className="h-80 bg-white border border-gray-200 rounded-xl p-4">
          <ResponsiveContainer>
            <BarChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
              <XAxis 
                dataKey="x" 
                tickFormatter={(v)=>v.toFixed(1)}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                allowDecimals={false}
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                formatter={(v, n, p)=>[v, `bin≈${p.payload.x.toFixed(1)}`]}
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '12px'
                }}
              />
              <Bar dataKey="count" isAnimationActive={false}>
                <LabelList 
                  dataKey="count" 
                  position="top" 
                  className="text-xs fill-gray-600" 
                />
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}