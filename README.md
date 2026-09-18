# RetainIQ Buyer Intelligence Dashboard

Machine Learning–based buyer segmentation and investment profiling for the
RetainIQ real estate platform, built as a Unified Mentor capstone project.

## What this does

Applies K-Means clustering (K=6, validated with elbow method + silhouette
scoring and cross-checked against hierarchical clustering) to 2,000 buyer
records merged with 10,000 property transactions, surfacing six distinct
buyer archetypes:

| Segment | Key characteristic |
|---|---|
| Portfolio Investors | Highest volume (avg 7.7 units), multi-tower, office-heavy |
| Luxury Buyers | Highest avg price-per-unit ($434K), large floor area |
| Global Buyers | Internationally diverse — Canada, Belgium, Australia |
| Corporate Buyers | 100% company clients, structured acquisition |
| Mid-Market Buyers | Largest group; moderate spend, mixed purpose |
| Domestic Home Buyers | US-centric, entry-level, home-use focus |

## Folder structure

```
retainiq_app/
├── app.py
├── clustered.csv          # output of the ML pipeline (run once offline)
├── clients.csv
├── properties.csv
├── requirements.txt
├── .env.example
├── components/
│   ├── charts.py
│   ├── filters.py
│   └── kpi_cards.py
├── utils/
│   ├── data_loader.py
│   └── formatters.py
└── styles/
    └── theme.py
```

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (free public link)

Push to a public GitHub repo, then go to share.streamlit.io.
Point it at app.py — the CSV files are included in the repo.
