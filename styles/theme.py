"""
Parcl brand design tokens.

Parcl's website is dark/near-black with a white wordmark and a vivid
green accent. The internal analytics UI carries that through: dark card
surfaces, tight borders, white primary text, green for positive signals,
red/amber for risk. Multi-colour segment palette keeps each cluster
visually distinct across all charts.
"""

import streamlit as st

# ── Brand tokens ─────────────────────────────────────────────────────
BG          = "#0D0D0D"   # near-black page background
CARD        = "#161616"   # card surfaces
CARD_RAISED = "#1E1E1E"   # slightly lighter card (nested sections)
BORDER      = "#2A2A2A"
GREEN       = "#00D97E"   # Parcl primary accent — positive / primary
AMBER       = "#F4C542"   # warning / second accent
RED         = "#E84560"   # risk / alert
TEAL        = "#17BEBB"
WHITE       = "#FFFFFF"
MUTED       = "#888888"
TEXT        = "#FFFFFF"
TEXT_SEC    = "#AAAAAA"
FONT        = "'Inter', 'Poppins', sans-serif"

# ── Segment colours ───────────────────────────────────────────────────
SEG_COLORS = {
    "Global Buyers":        "#17BEBB",
    "Domestic Home Buyers": "#6BA292",
    "Mid-Market Buyers":    "#F4C542",
    "Luxury Buyers":        "#F28C38",
    "Corporate Buyers":     "#8FD6D2",
    "Portfolio Investors":  "#E84560",
}

# ── Plotly base layout — ONLY safe non-conflicting keys ──────────────
# legend, xaxis, yaxis are intentionally excluded here because individual
# chart functions need to customise them. Passing them in PLOTLY_LAYOUT
# AND in the chart's own update_layout() call causes:
#   TypeError: got multiple values for keyword argument 'legend'
# Instead, _apply_theme() in charts.py sets axes separately via a second
# update_layout() call so there is never a duplicate keyword.
PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, Poppins, sans-serif", color=WHITE, size=13),
    plot_bgcolor=CARD,
    paper_bgcolor=CARD,
    margin=dict(l=12, r=12, t=36, b=12),
)


def inject_css():
    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: {FONT};
        color: {TEXT};
        background-color: {BG};
    }}
    .main {{ background-color: {BG}; }}

    /* Hide Streamlit's default top header bar so it doesn't overlap content */
    header[data-testid="stHeader"] {{
        background: {BG} !important;
        border-bottom: 1px solid {BORDER} !important;
    }}

    .block-container {{
        padding: 5rem 2.2rem 3rem 2.2rem;
        max-width: 100%;
    }}

    /* ── Sidebar ─────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {{
        background: #111111 !important;
        border-right: 1px solid {BORDER} !important;
    }}
    section[data-testid="stSidebar"] * {{ color: {WHITE} !important; }}
    section[data-testid="stSidebar"] .stMultiSelect [data-baseweb="select"] {{
        background: {CARD_RAISED} !important;
        border-radius: 8px !important;
        border: 1px solid {BORDER} !important;
    }}

    /* Override the default salmon-red multiselect tags — they look like
       error/delete warnings. Dark teal pill = selected state, not alert. */
    section[data-testid="stSidebar"] [data-baseweb="tag"] {{
        background-color: rgba(23,190,187,0.18) !important;
        border: 1px solid rgba(23,190,187,0.45) !important;
        border-radius: 6px !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="tag"] span {{
        color: #17BEBB !important;
        font-weight: 600 !important;
    }}
    section[data-testid="stSidebar"] [data-baseweb="tag"] [role="presentation"] {{
        color: #17BEBB !important;
    }}
    section[data-testid="stSidebar"] hr {{ border-color: {BORDER}; }}
    .sidebar-brand {{
        font-size: 1.25rem;
        font-weight: 800;
        color: {WHITE} !important;
        letter-spacing: -0.02em;
    }}
    .sidebar-brand span {{ color: {GREEN} !important; }}
    .sidebar-caption {{
        font-size: 0.72rem;
        color: {MUTED} !important;
        margin-bottom: 1.2rem;
    }}
    .filter-head {{
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {MUTED} !important;
        margin: 1rem 0 0.2rem 0;
    }}

    /* ── Page header ─────────────────────────────────────────────── */
    .ph-title {{
        font-size: 1.6rem;
        font-weight: 800;
        color: {WHITE};
        letter-spacing: -0.025em;
        margin: 0;
    }}
    .ph-title span {{ color: {GREEN}; }}
    .ph-sub {{
        font-size: 0.83rem;
        color: {MUTED};
        margin: 0.2rem 0 0 0;
    }}
    .ph-badge {{
        display: inline-block;
        background: {GREEN};
        color: #000 !important;
        font-size: 0.68rem;
        font-weight: 700;
        padding: 0.2rem 0.75rem;
        border-radius: 20px;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }}

    /* ── KPI cards ───────────────────────────────────────────────── */
    .kpi {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.3rem 1.5rem 1.2rem 1.5rem;
        position: relative;
        overflow: hidden;
    }}
    .kpi-bar {{
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 12px 12px 0 0;
    }}
    .kpi-label {{
        font-size: 0.67rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: {MUTED};
        margin-bottom: 0.45rem;
    }}
    .kpi-val {{
        font-size: 2rem;
        font-weight: 800;
        color: {WHITE};
        letter-spacing: -0.02em;
        line-height: 1.0;
    }}
    .kpi-sub {{
        font-size: 0.74rem;
        color: {MUTED};
        margin-top: 0.35rem;
    }}

    /* ── Chart cards ─────────────────────────────────────────────── */
    .card {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 1.3rem 1.5rem 0.5rem 1.5rem;
        margin-bottom: 1rem;
    }}
    .card-title {{
        font-size: 0.9rem;
        font-weight: 700;
        color: {WHITE};
        margin-bottom: 0.12rem;
    }}
    .card-sub {{
        font-size: 0.73rem;
        color: {MUTED};
        margin-bottom: 0.5rem;
    }}

    /* ── Segment badge pills ─────────────────────────────────────── */
    .seg-pill {{
        display: inline-block;
        padding: 0.2rem 0.7rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 0.15rem;
    }}

    /* ── Tabs ────────────────────────────────────────────────────── */
    div.stTabs [data-baseweb="tab-list"] {{
        gap: 0.3rem;
        border-bottom: 1px solid {BORDER};
        background: transparent;
    }}
    div.stTabs [data-baseweb="tab"] {{
        color: {MUTED};
        font-weight: 600;
        font-size: 0.84rem;
        padding: 0.45rem 1rem;
        border-radius: 6px 6px 0 0;
        background: transparent;
        border: none;
    }}
    div.stTabs [aria-selected="true"] {{
        color: {GREEN} !important;
        background: rgba(0,217,126,0.08) !important;
        border-bottom: 2px solid {GREEN} !important;
    }}

    div[data-testid="stHorizontalBlock"] {{ gap: 1rem; }}
    .spacer {{ margin-top: 1.2rem; }}
    hr.divider {{ border: none; border-top: 1px solid {BORDER}; margin: 0.7rem 0 1.4rem 0; }}
    </style>
    """, unsafe_allow_html=True)
