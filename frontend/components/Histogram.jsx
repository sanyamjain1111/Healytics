'use client';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';

function normalizeBins(hist) {
  // support various server shapes
  const bins = hist.bins || hist.hist || hist.data || [];
  return bins.map(b => ({
    x: b.bin_start ?? b.left ?? b.start ?? b.x ?? 0,
    x2: b.bin_end ?? b.right ?? b.end ?? (b.x2 ?? 0),
    count: b.count ?? b.y ?? b.freq ?? 0
  }));
}

export function Histogram({ hist }) {
  const data = normalizeBins(hist);
  const title = hist.column || hist.name || 'Distribution';
  return (
    <div className="card chart-card">
      <h3>{title}</h3>
      <small className="muted">x: value range • y: count</small>
      <div style={{height:240}}>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="x" label={{ value:'Value (bin start)', position:'insideBottom', offset:-2 }} />
            <YAxis label={{ value: 'Count', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Bar dataKey="count" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
