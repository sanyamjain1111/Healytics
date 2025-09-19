
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime
from jinja2 import Template
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import utils
from ..paths import REPORT_DIR

HTML_TEMPLATE = Template("""
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>{{ title }}</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; }
    h1, h2 { margin: 0 0 8px 0; }
    .meta { color: #666; margin-bottom: 24px; }
    .code { font-family: monospace; white-space: pre-wrap; background: #f6f8fa; padding: 12px; border-radius: 8px; }
    .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
    img { max-width: 100%; border: 1px solid #ddd; border-radius: 6px; }
  </style>
</head>
<body>
  <h1>{{ title }}</h1>
  <div class="meta">Model: <b>{{ model_name }}</b> · Generated: {{ ts }}</div>
  <h2>Metrics</h2>
  <div class="code">{{ metrics_json }}</div>

  {% if shap_rel %}
  <h2>SHAP Summary</h2>
  <img src="{{ shap_rel }}" alt="SHAP summary"/>
  {% endif %}
</body>
</html>
""")

def _rel(from_path: Path, to_path: Path) -> str:
    try:
        return str(to_path.relative_to(from_path.parent))
    except Exception:
        return str(to_path)

def generate_reports(model_name: str, artifacts: Dict[str, str]) -> Dict[str, str]:
    mdir = Path(artifacts.get("metrics", "")).parent if artifacts.get("metrics") else REPORT_DIR
    rdir = REPORT_DIR / mdir.name
    rdir.mkdir(parents=True, exist_ok=True)

    # HTML
    ts = datetime.utcnow().isoformat()
    metrics_json = Path(artifacts["metrics"]).read_text() if artifacts.get("metrics") else "{}"
    html = HTML_TEMPLATE.render(
        title="Model Report",
        model_name=model_name,
        ts=ts,
        metrics_json=metrics_json,
        shap_rel=_rel(rdir, Path(artifacts["shap"])) if artifacts.get("shap") else ""
    )
    html_path = rdir / "report.html"
    html_path.write_text(html, encoding="utf-8")

    # PDF
    pdf_path = rdir / "report.pdf"
    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 50, "Model Report")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 70, f"Model: {model_name}")
    c.drawString(40, height - 85, f"Generated: {ts}")
    # Metrics block
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, height - 115, "Metrics:")
    c.setFont("Helvetica", 8)
    txt = c.beginText(40, height - 130)
    for line in metrics_json.splitlines()[:60]:
        txt.textLine(line[:120])
    c.drawText(txt)
    # SHAP image
    shap_path = artifacts.get("shap")
    if shap_path and Path(shap_path).exists():
        try:
            c.drawImage(ImageReader(shap_path), 40, 120, width=520, height=300, preserveAspectRatio=True, anchor='c')
        except Exception:
            pass
    c.showPage()
    c.save()

    return {"html": str(html_path), "pdf": str(pdf_path)}
