# Medical IntelliAnalytics – Frontend

Next.js App Router UI for:
- Uploading datasets
- Viewing dataset summaries & histograms (with axis labels)
- Generating strategy (Gemini or static fallback)
- Ad‑hoc patient predictions (random/specific)
- SQL via DuckDB on backend

## Configure
Create `.env.local` if needed:
```
NEXT_PUBLIC_API_BASE=http://localhost:8000
```

## Run
```
npm i
npm run dev
```

## Endpoint map
- `GET /datasets`
- `POST /datasets/upload`
- `GET /datasets/{id}/summary`
- `GET /datasets/{id}/columns`
- `GET /analytics/histograms?dataset_id=ID&columns=age,glucose&bins=20`
- `POST /analytics/ad-hoc` body: `{ dataset_id, sql }`
- `GET /strategies` (fallback)
- `POST /strategy/generate` body: `{ dataset_id }`
- `GET /adhoc/random?dataset_id=ID`
- `POST /adhoc/predict` body: `{ dataset_id, strategy_id, patient_id? }`
```
