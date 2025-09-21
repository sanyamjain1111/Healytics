import React from 'react';
import { BarChart, Bar, Cell, XAxis, YAxis, Tooltip, ResponsiveContainer, LabelList, ReferenceLine } from 'recharts';
import { Activity, TrendingUp } from 'lucide-react';

const bands = [
  { key: 'very-low', to: 0.2, color: '#16a34a', label: 'Very Low' },
  { key: 'low', to: 0.4, color: '#84cc16', label: 'Low' },
  { key: 'medium', to: 0.6, color: '#eab308', label: 'Medium' },
  { key: 'medium-high', to: 0.8, color: '#f97316', label: 'Medium-High' },
  { key: 'high', to: 1.01, color: '#dc2626', label: 'High' },
];

function bandFor(x) {
  for (const b of bands) { if (x < b.to) return b; }
  return bands[bands.length-1];
}

export default function RiskHistogram({ scores=[], threshold=null, title }) {
  const nBins = 20;
  const counts = Array.from({length:nBins}, (_,i)=>({ bin: (i+0.5)/nBins, count: 0 }));
  for (const s of scores) {
    const x = Math.max(0, Math.min(0.999999, s));
    const idx = Math.floor(x*nBins);
    counts[idx].count += 1;
  }
  const data = counts.map(d => ({ ...d, fill: bandFor(d.bin).color }));
  const thrX = threshold == null ? null : Math.ceil(threshold*nBins)/nBins;

  // Calculate totals for each band
  const total = data.reduce((a,x)=>a+(x.count||0),0) || 1;
  const bandCounts = {};
  data.forEach(d => {
    const band = bandFor(d.bin);
    bandCounts[band.key] = (bandCounts[band.key] || 0) + d.count;
  });

  return (
    <div className="bg-gradient-to-br from-white to-violet-50 border border-violet-200 rounded-2xl p-6 hover:shadow-lg transition-all duration-200">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 bg-gradient-to-r from-violet-500 to-purple-500 rounded-xl">
          <Activity className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-xl font-bold text-gray-800">{title}</h3>
      </div>
      
      <div className="text-sm text-gray-600 mb-4 bg-gray-50 p-3 rounded-xl border border-gray-200">
        Risk bands: &lt;0.2 Very Low, 0.2–0.4 Low, 0.4–0.6 Medium, 0.6–0.8 Medium-High, ≥0.8 High
      </div>
      
      <div className="w-full">
        {/* Risk Band Legend */}
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 mb-6">
          {bands.map(b=>{
            const c = bandCounts[b.key] || 0;
            const pct = ((c/total)*100).toFixed(1);
            return (
              <div key={b.key} className="bg-white border border-gray-200 rounded-xl p-3 hover:shadow-md transition-all duration-200">
                <div className="flex items-center gap-2 mb-2">
                  <div className="w-4 h-4 rounded-full" style={{backgroundColor:b.color}} />
                  <div className="text-sm font-semibold text-gray-700">{b.label}</div>
                </div>
                <div className="text-lg font-bold text-gray-800">{c}</div>
                <div className="text-xs text-gray-500">({pct}%)</div>
              </div>
            );
          })}
        </div>
        
        {/* Chart */}
        <div className="h-80 bg-white border border-gray-200 rounded-xl p-4">
          <ResponsiveContainer>
            <BarChart data={data} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
              <XAxis 
                dataKey="bin" 
                tickFormatter={(v)=>v.toFixed(2)}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                allowDecimals={false}
                tick={{ fontSize: 12 }}
              />
              <Tooltip 
                formatter={(v, n, p)=>[v, `bin=${p.payload.bin.toFixed(2)}`]}
                contentStyle={{
                  backgroundColor: 'white',
                  border: '1px solid #d1d5db',
                  borderRadius: '8px',
                  fontSize: '12px'
                }}
              />
              {thrX !== null && (
                <ReferenceLine 
                  x={thrX} 
                  stroke="#6366f1" 
                  strokeDasharray="4 4" 
                  strokeWidth={2}
                  label={{
                    value: `threshold=${threshold?.toFixed(3)}`,
                    position: 'top',
                    style: { 
                      fontSize: '12px', 
                      fill: '#6366f1',
                      fontWeight: 'bold'
                    }
                  }}
                />
              )}
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