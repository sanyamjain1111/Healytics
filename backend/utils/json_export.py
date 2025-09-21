
import os, json, datetime
def export_json(dataset_id: int, kind: str, payload: dict) -> str:
    # kind in {"risk_prediction", "anomaly_detection"}
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    base = f"artifacts/analysis/dataset_{dataset_id}/{ts}"
    os.makedirs(base, exist_ok=True)
    path = f"{base}/{kind}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return path
