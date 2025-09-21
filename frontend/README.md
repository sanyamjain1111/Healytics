# Healytics – Frontend

Light-themed React (Vite + Tailwind + Recharts) dashboard matching your backend.

## Quick start

```bash
npm i
npm run dev
```

Set the **API Base** at the top right (default: `http://127.0.0.1:8000`).

## Features

- Upload & list datasets (no SQL tab).
- Generate strategies (shows id + JSON).
- Run analysis → loads risk & anomaly artifacts and renders per-model lists with histograms colored by risk bands (green→red).
- Reports generator (renders JSON returned by `/reports/generate`).
- Patient search (by id) using `/analytics/adhoc/predict`.
- Ad-hoc predictor (load a sample, edit values, predict).

## Optional backend helper

Add `/artifacts/get?path=...` to serve analysis JSON if you don’t already serve the `artifacts/` directory.
