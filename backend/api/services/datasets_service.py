from __future__ import annotations
import os, json, pathlib, datetime
from typing import Dict, Any, Optional, List
import pandas as pd

DATA_DIR = os.environ.get("DATA_DIR", "./data/uploads")
REGISTRY_PATH = os.environ.get("DATASET_REGISTRY", "./data/registry.json")

class DatasetRegistry:
    def __init__(self, data_dir: str, registry_path: str):
        self.data_dir = data_dir
        self.registry_path = registry_path
        os.makedirs(os.path.dirname(registry_path), exist_ok=True)
        os.makedirs(self.data_dir, exist_ok=True)
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump({"datasets": {}}, f)

    def _load(self) -> Dict[str, Any]:
        with open(self.registry_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: Dict[str, Any]):
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def list(self) -> List[Dict[str, Any]]:
        data = self._load()
        return list(data.get("datasets", {}).values())

    def get(self, dataset_id: str) -> Optional[Dict[str, Any]]:
        data = self._load()
        return data.get("datasets", {}).get(dataset_id)

    def path_for(self, dataset_id: str) -> str:
        ds = self.get(dataset_id)
        if not ds:
            raise FileNotFoundError("Unknown dataset")
        return ds["path"]

    def _new_id(self, name: str) -> str:
        base = pathlib.Path(name).stem.lower().replace(" ", "-")
        base = "".join(ch for ch in base if ch.isalnum() or ch in ("-", "_"))
        i = 1
        cand = base or "dataset"
        data = self._load()
        existing = set(data.get("datasets", {}).keys())
        while cand in existing:
            i += 1
            cand = f"{base}-{i}"
        return cand

    def add_from_path(self, path: str, name: Optional[str] = None) -> Dict[str, Any]:
        df = load_dataframe(path)
        dataset_id = self._new_id(name or os.path.basename(path))
        meta = {
            "id": dataset_id,
            "name": name or os.path.basename(path),
            "path": os.path.abspath(path),
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "rows": int(len(df)),
            "cols": int(len(df.columns)),
            "columns": [{"name": c, "dtype": str(df[c].dtype)} for c in df.columns],
        }
        data = self._load()
        data.setdefault("datasets", {})[dataset_id] = meta
        self._save(data)
        return meta

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def load_dataframe(path: str) -> pd.DataFrame:
    ext = os.path.splitext(path)[1].lower()
    if ext in (".csv", ""):
        return pd.read_csv(path)
    if ext in (".parquet", ".pq", ".feather"):
        try:
            return pd.read_parquet(path)
        except Exception:
            # feather fallback
            import pyarrow.feather as feather
            return feather.read_feather(path)
    if ext in (".xlsx", ".xls"):
        return pd.read_excel(path)
    # default try CSV
    return pd.read_csv(path)

registry = DatasetRegistry(DATA_DIR, REGISTRY_PATH)