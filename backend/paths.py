
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE / "artifacts"
REPORT_DIR = BASE / "reports"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
REPORT_DIR.mkdir(parents=True, exist_ok=True)
