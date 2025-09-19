from typing import Optional, Iterable, Tuple
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin

class IQRClippingTransformer(BaseEstimator, TransformerMixin):
    """
    Robust outlier clipping using the IQR rule, safe for both pandas DataFrames and NumPy arrays.
    - If input is a DataFrame: preserves index/columns.
    - If input is an array: returns an array.
    - Handles constant/near-constant columns gracefully.
    """
    def __init__(self, q_low: float = 0.25, q_high: float = 0.75, k: float = 1.5):
        self.q_low = q_low
        self.q_high = q_high
        self.k = k
        self.bounds_: Optional[np.ndarray] = None  # shape (n_features, 2)
        self.is_dataframe_: bool = True
        self.columns_: Optional[Iterable[str]] = None

    def _to_numpy(self, X) -> Tuple[np.ndarray, Optional[pd.Index], Optional[pd.Index]]:
        if isinstance(X, pd.DataFrame):
            self.is_dataframe_ = True
            return X.to_numpy(), X.index, X.columns
        else:
            self.is_dataframe_ = False
            return np.asarray(X), None, None

    def fit(self, X, y=None):
        arr, _, cols = self._to_numpy(X)
        n_features = arr.shape[1]
        self.columns_ = cols
        bounds = np.zeros((n_features, 2), dtype=float)

        # Compute per-feature IQR bounds with NaN-robust percentiles
        for j in range(n_features):
            col = arr[:, j].astype(float)
            q1 = np.nanpercentile(col, self.q_low * 100.0)
            q3 = np.nanpercentile(col, self.q_high * 100.0)
            iqr = q3 - q1
            if not np.isfinite(iqr) or iqr == 0:
                # constant or degenerate: just bound by finite min/max (or leave as is)
                finite = col[np.isfinite(col)]
                if finite.size:
                    lo, hi = np.nanmin(finite), np.nanmax(finite)
                else:
                    lo, hi = q1, q3
            else:
                lo = q1 - self.k * iqr
                hi = q3 + self.k * iqr
            bounds[j, 0] = lo
            bounds[j, 1] = hi

        self.bounds_ = bounds
        return self

    def transform(self, X):
        if self.bounds_ is None:
            raise RuntimeError("IQRClippingTransformer must be fit before transform().")
        arr, idx, cols = self._to_numpy(X)
        clipped = np.clip(arr, self.bounds_[:, 0], self.bounds_[:, 1])

        if self.is_dataframe_:
            return pd.DataFrame(clipped, index=idx, columns=cols)
        return clipped
