"""
Data loading and ML pipeline.

Loads the pre-clustered CSV (produced by the offline training script)
rather than re-running K-Means on every page load — clustering on 2,000
rows takes a few seconds, which is noticeable in a dashboard context.
The clustered.csv is the single source of truth for the UI.
"""

import os
import pandas as pd
import streamlit as st


class DataLoadError(Exception):
    pass


@st.cache_data(show_spinner=False)
def load_clustered(path: str = "clustered.csv") -> pd.DataFrame:
    if not os.path.exists(path):
        raise DataLoadError(
            f"Clustered dataset not found at '{path}'. "
            "Make sure clustered.csv is in the same folder as app.py."
        )
    df = pd.read_csv(path)
    required = ["client_id", "cluster", "segment_name", "age",
                "total_spend", "total_units", "avg_price",
                "satisfaction_score", "country", "region",
                "acquisition_purpose", "loan_applied", "client_type"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise DataLoadError(f"Missing columns in clustered.csv: {missing}")
    return df


@st.cache_data(show_spinner=False)
def load_properties(path: str = "properties.csv") -> pd.DataFrame:
    if not os.path.exists(path):
        return pd.DataFrame()
    df = pd.read_csv(path)
    df["sale_price_clean"] = (
        df["sale_price"].str.replace("$", "", regex=False)
                        .str.replace(",", "", regex=False)
                        .astype(float)
    )
    return df
