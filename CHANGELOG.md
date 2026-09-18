# Changelog

## v1.0.0 — Initial build

- Full ML pipeline: data cleaning, feature engineering (13 features),
  StandardScaler normalisation, K-Means (K=6 via elbow + silhouette),
  hierarchical validation against Ward-linkage clustering
- Six buyer segments identified and named: Portfolio Investors, Luxury
  Buyers, Global Buyers, Corporate Buyers, Mid-Market Buyers,
  Domestic Home Buyers
- Pre-clustered CSV exported as single source of truth for the dashboard

## v1.1.0 — Dashboard + Research Paper

- Streamlit dashboard in Parcl's dark brand (near-black, green accent)
- Modular structure: styles/, utils/, components/, app.py
- Four tabs: Segmentation Overview, Investor Behaviour, Geographic
  Analysis, Segment Insights (radar + per-segment stat cards + drill-down)
- Seven KPIs across two rows with per-metric accent colour bars
- Sidebar filters: country, region, acquisition purpose, client type, segment
- PDF research paper (7 sections, 8 embedded charts, segment profile table,
  strategic recommendations)
