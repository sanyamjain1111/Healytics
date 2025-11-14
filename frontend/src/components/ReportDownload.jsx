import React, { useState } from 'react';
import { Download, FileText, Globe, Loader2 } from 'lucide-react';

function ReportDownloader({ report, datasetName }) {
  const [downloading, setDownloading] = useState(false);
  const [error, setError] = useState('');

  const generateHTML = () => {
    const s = report.summary || {};
    const risk = s.risk_overview || {};
    const counts = risk.counts || {};
    const insights = report.insights || {};
    const datasetDisplay = datasetName || `Dataset ${report.dataset_id ?? s.dataset_id ?? '-'}`;

    const models = Object.entries(counts).map(([name, obj]) => ({
      model: name,
      positives: obj.positives ?? obj.n ?? 0,
      total: obj.total ?? obj.n ?? 0,
      rate: (obj.positives != null && obj.total) ? (obj.positives / obj.total) : null,
    }));
    const cls = models.filter(m => m.total && m.rate !== null);

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clinical Analysis Report - Dataset ${report.dataset_id ?? s.dataset_id ?? '-'}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 40px 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }
        
        .header .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .stat-card .value {
            font-size: 2.5em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .stat-card .label {
            font-size: 0.9em;
            color: #555;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stat-card .sub {
            font-size: 0.75em;
            color: #777;
            margin-top: 5px;
        }
        
        .section {
            margin-bottom: 40px;
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            border-left: 5px solid #667eea;
        }
        
        .section h2 {
            color: #667eea;
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .section h2::before {
            content: "▶";
            font-size: 0.6em;
        }
        
        .executive-summary {
            font-size: 1.1em;
            line-height: 1.8;
            color: #444;
            background: white;
            padding: 25px;
            border-radius: 10px;
            border: 2px solid #e0e0e0;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        thead {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85em;
            letter-spacing: 1px;
        }
        
        td {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        tbody tr:hover {
            background-color: #f5f7fa;
        }
        
        tbody tr:last-child td {
            border-bottom: none;
        }
        
        .badge {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9em;
        }
        
        .badge-green {
            background: #d4edda;
            color: #155724;
        }
        
        .badge-blue {
            background: #d1ecf1;
            color: #0c5460;
        }
        
        .badge-purple {
            background: #e2d9f3;
            color: #5a3d8a;
        }
        
        .findings-list {
            list-style: none;
        }
        
        .findings-list li {
            background: white;
            margin-bottom: 15px;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        
        .findings-list li::before {
            content: "✓";
            color: #667eea;
            font-weight: bold;
            margin-right: 10px;
            font-size: 1.2em;
        }
        
        .params-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        .param-item {
            background: white;
            padding: 15px 20px;
            border-radius: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid #e0e0e0;
        }
        
        .param-label {
            font-weight: 600;
            color: #555;
        }
        
        .param-value {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-weight: 600;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            border-top: 2px solid #e0e0e0;
        }
        
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .container {
                box-shadow: none;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Clinical Analysis Report</h1>
            <div class="subtitle">Dataset ${report.dataset_id ?? s.dataset_id ?? '-'} | Generated ${new Date().toLocaleString()}</div>
        </div>
        
        <div class="content">
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="value">${report.dataset_id ?? s.dataset_id ?? '-'}</div>
                    <div class="label">Dataset ID</div>
                </div>
                <div class="stat-card">
                    <div class="value">${risk.strategy_id ?? s.strategy_id ?? '-'}</div>
                    <div class="label">Strategy ID</div>
                </div>
                <div class="stat-card">
                    <div class="value">${(risk.selected_models || []).length}</div>
                    <div class="label">Selected Models</div>
                </div>
                <div class="stat-card">
                    <div class="value">${s.anomaly_overview?.n_anomalies ?? 0} / ${s.anomaly_overview?.total ?? 0}</div>
                    <div class="label">Anomalies</div>
                    <div class="sub">(detected / total)</div>
                </div>
            </div>
            
            ${insights.executive_summary ? `
            <div class="section">
                <h2>Executive Summary</h2>
                <div class="executive-summary">${insights.executive_summary}</div>
            </div>
            ` : ''}
            
            ${cls.length > 0 ? `
            <div class="section">
                <h2>Model Performance</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Model</th>
                            <th>Positives</th>
                            <th>Total</th>
                            <th>Rate</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${cls.map(m => `
                        <tr>
                            <td><strong>${m.model}</strong></td>
                            <td><span class="badge badge-green">${m.positives}</span></td>
                            <td><span class="badge badge-blue">${m.total}</span></td>
                            <td><span class="badge badge-purple">${m.rate != null ? (m.rate * 100).toFixed(2) + '%' : '-'}</span></td>
                        </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
            ` : ''}
            
            ${Array.isArray(insights.key_findings) && insights.key_findings.length > 0 ? `
            <div class="section">
                <h2>Key Findings</h2>
                <ul class="findings-list">
                    ${insights.key_findings.map(finding => `<li>${finding}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
            
            ${Array.isArray(insights.recommendations) && insights.recommendations.length > 0 ? `
            <div class="section">
                <h2>Recommendations</h2>
                <ul class="findings-list">
                    ${insights.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
            
            ${s.params ? `
            <div class="section">
                <h2>Analysis Parameters</h2>
                <div class="params-grid">
                    ${Object.entries(s.params).map(([k, v]) => `
                    <div class="param-item">
                        <span class="param-label">${k}</span>
                        <span class="param-value">${v}</span>
                    </div>
                    `).join('')}
                </div>
            </div>
            ` : ''}
        </div>
        
        <div class="footer">
            <p>Clinical Analysis Report System | Generated on ${new Date().toLocaleDateString()}</p>
        </div>
    </div>
</body>
</html>`;
  };

  const downloadHTML = () => {
    try {
      const html = generateHTML();
      const blob = new Blob([html], { type: 'text/html' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `clinical_report_${report.dataset_id || 'unknown'}_${Date.now()}.html`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('HTML download error:', err);
      setError('Failed to download HTML');
    }
  };

  const downloadPDF = async () => {
    setDownloading(true);
    setError('');
    
    try {
      console.log('Starting PDF generation...');
      
      // Dynamically import jsPDF and autoTable
      const jsPDFModule = await import('jspdf');
      const jsPDF = jsPDFModule.default;
      
      // Import autoTable - this adds the method to jsPDF prototype
      const autoTableModule = await import('jspdf-autotable');
      
      console.log('jsPDF loaded successfully');
      
      const s = report.summary || {};
      const risk = s.risk_overview || {};
      const counts = risk.counts || {};
      const insights = report.insights || {};

      const models = Object.entries(counts).map(([name, obj]) => ({
        model: name,
        positives: obj.positives ?? obj.n ?? 0,
        total: obj.total ?? obj.n ?? 0,
        rate: (obj.positives != null && obj.total) ? (obj.positives / obj.total) : null,
      }));
      const cls = models.filter(m => m.total && m.rate !== null);

      console.log('Creating PDF document...');
      const doc = new jsPDF();
      let yPos = 20;

      // Header with gradient effect (simulated)
      doc.setFillColor(102, 126, 234);
      doc.rect(0, 0, 210, 50, 'F');
      doc.setTextColor(255, 255, 255);
      doc.setFontSize(24);
      doc.setFont(undefined, 'bold');
      doc.text('Clinical Analysis Report', 105, 25, { align: 'center' });
      doc.setFontSize(12);
      doc.setFont(undefined, 'normal');
      doc.text(`Dataset ${report.dataset_id ?? s.dataset_id ?? '-'} | ${new Date().toLocaleDateString()}`, 105, 38, { align: 'center' });

      yPos = 60;
      doc.setTextColor(0, 0, 0);

      // Stats boxes
      doc.setFontSize(10);
      const stats = [
        { label: 'Dataset ID', value: String(report.dataset_id ?? s.dataset_id ?? '-') },
        { label: 'Strategy ID', value: String(risk.strategy_id ?? s.strategy_id ?? '-') },
        { label: 'Models', value: String((risk.selected_models || []).length) },
        { label: 'Anomalies', value: `${s.anomaly_overview?.n_anomalies ?? 0}/${s.anomaly_overview?.total ?? 0}` }
      ];

      const boxWidth = 45;
      const boxHeight = 20;
      const startX = 15;
      stats.forEach((stat, i) => {
        const x = startX + (i * (boxWidth + 2));
        doc.setFillColor(245, 247, 250);
        doc.roundedRect(x, yPos, boxWidth, boxHeight, 3, 3, 'FD');
        doc.setFontSize(16);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(102, 126, 234);
        doc.text(stat.value, x + boxWidth / 2, yPos + 10, { align: 'center' });
        doc.setFontSize(8);
        doc.setFont(undefined, 'normal');
        doc.setTextColor(85, 85, 85);
        doc.text(stat.label, x + boxWidth / 2, yPos + 16, { align: 'center' });
      });

      yPos += 30;
      doc.setTextColor(0, 0, 0);

      // Executive Summary
      if (insights.executive_summary) {
        if (yPos > 250) {
          doc.addPage();
          yPos = 20;
        }
        
        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(102, 126, 234);
        doc.text('Executive Summary', 15, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setFont(undefined, 'normal');
        doc.setTextColor(68, 68, 68);
        const summaryLines = doc.splitTextToSize(insights.executive_summary, 180);
        doc.text(summaryLines, 15, yPos);
        yPos += summaryLines.length * 5 + 10;
      }

      // Model Performance Table
      if (cls.length > 0) {
        if (yPos > 250) {
          doc.addPage();
          yPos = 20;
        }

        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(102, 126, 234);
        doc.text('Model Performance', 15, yPos);
        yPos += 8;

        try {
          // Try using autoTable if available
          if (typeof doc.autoTable === 'function') {
            doc.autoTable({
              startY: yPos,
              head: [['Model', 'Positives', 'Total', 'Rate']],
              body: cls.map(m => [
                m.model,
                String(m.positives),
                String(m.total),
                m.rate != null ? (m.rate * 100).toFixed(2) + '%' : '-'
              ]),
              theme: 'striped',
              headStyles: {
                fillColor: [102, 126, 234],
                textColor: [255, 255, 255],
                fontStyle: 'bold',
                halign: 'left'
              },
              alternateRowStyles: {
                fillColor: [248, 249, 250]
              },
              styles: {
                fontSize: 9,
                cellPadding: 5
              }
            });
            yPos = doc.lastAutoTable.finalY + 15;
          } else {
            throw new Error('autoTable not available');
          }
        } catch (tableErr) {
          // Fallback: manual table drawing
          console.log('Using manual table drawing');
          doc.setFontSize(10);
          doc.setFont(undefined, 'bold');
          
          // Header
          doc.setFillColor(102, 126, 234);
          doc.rect(15, yPos, 180, 8, 'F');
          doc.setTextColor(255, 255, 255);
          doc.text('Model', 20, yPos + 5);
          doc.text('Positives', 70, yPos + 5);
          doc.text('Total', 110, yPos + 5);
          doc.text('Rate', 150, yPos + 5);
          yPos += 10;
          
          // Body
          doc.setFont(undefined, 'normal');
          doc.setTextColor(0, 0, 0);
          cls.forEach((m, i) => {
            if (yPos > 270) {
              doc.addPage();
              yPos = 20;
            }
            
            if (i % 2 === 0) {
              doc.setFillColor(248, 249, 250);
              doc.rect(15, yPos - 3, 180, 8, 'F');
            }
            
            doc.text(m.model, 20, yPos + 2);
            doc.text(String(m.positives), 70, yPos + 2);
            doc.text(String(m.total), 110, yPos + 2);
            doc.text(m.rate != null ? (m.rate * 100).toFixed(2) + '%' : '-', 150, yPos + 2);
            yPos += 8;
          });
          
          yPos += 10;
        }
      }

      // Key Findings
      if (Array.isArray(insights.key_findings) && insights.key_findings.length > 0) {
        if (yPos > 250) {
          doc.addPage();
          yPos = 20;
        }

        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(102, 126, 234);
        doc.text('Key Findings', 15, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setFont(undefined, 'normal');
        doc.setTextColor(68, 68, 68);

        insights.key_findings.forEach((finding, i) => {
          if (yPos > 270) {
            doc.addPage();
            yPos = 20;
          }
          doc.setTextColor(102, 126, 234);
          doc.text(`✓`, 15, yPos);
          doc.setTextColor(68, 68, 68);
          const lines = doc.splitTextToSize(finding, 175);
          doc.text(lines, 22, yPos);
          yPos += lines.length * 5 + 5;
        });
        
        yPos += 5;
      }

      // Recommendations
      if (Array.isArray(insights.recommendations) && insights.recommendations.length > 0) {
        if (yPos > 250) {
          doc.addPage();
          yPos = 20;
        }

        doc.setFontSize(14);
        doc.setFont(undefined, 'bold');
        doc.setTextColor(102, 126, 234);
        doc.text('Recommendations', 15, yPos);
        yPos += 8;

        doc.setFontSize(10);
        doc.setFont(undefined, 'normal');
        doc.setTextColor(68, 68, 68);

        insights.recommendations.forEach((rec, i) => {
          if (yPos > 270) {
            doc.addPage();
            yPos = 20;
          }
          doc.setTextColor(102, 126, 234);
          doc.text(`✓`, 15, yPos);
          doc.setTextColor(68, 68, 68);
          const lines = doc.splitTextToSize(rec, 175);
          doc.text(lines, 22, yPos);
          yPos += lines.length * 5 + 5;
        });
      }

      // Footer
      const pageCount = doc.internal.getNumberOfPages();
      for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(`Page ${i} of ${pageCount}`, 105, 287, { align: 'center' });
      }

      console.log('Saving PDF...');
      doc.save(`clinical_report_${report.dataset_id || 'unknown'}_${Date.now()}.pdf`);
      console.log('PDF saved successfully!');
      
    } catch (err) {
      console.error('PDF generation error:', err);
      setError(`Failed to generate PDF: ${err.message}`);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <div>
      <div className="flex gap-3">
        <button
          onClick={downloadHTML}
          className="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-700 hover:to-cyan-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
        >
          <Globe className="w-5 h-5" />
          Download HTML
        </button>
        
        <button
          onClick={downloadPDF}
          disabled={downloading}
          className={`flex items-center gap-2 px-6 py-3 font-semibold rounded-xl shadow-lg transition-all duration-200 ${
            downloading
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-red-600 to-pink-600 hover:from-red-700 hover:to-pink-700 text-white hover:shadow-xl transform hover:-translate-y-0.5'
          }`}
        >
          {downloading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              Generating PDF...
            </>
          ) : (
            <>
              <FileText className="w-5 h-5" />
              Download PDF
            </>
          )}
        </button>
      </div>
      
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl flex items-center gap-3">
          <div className="text-red-600 text-sm font-medium">{error}</div>
        </div>
      )}
    </div>
  );
}

export default ReportDownloader;