"""
Plotly chart builders — Parcl dark theme.

Key design decision: PLOTLY_LAYOUT only contains font/background/margin.
Axes (xaxis, yaxis) and legend are ALWAYS set via a separate second
update_layout() call inside _apply_theme(), never in the same call as
**PLOTLY_LAYOUT. This prevents:
  TypeError: got multiple values for keyword argument 'legend'
  TypeError: got multiple values for keyword argument 'xaxis'
which happen when both PLOTLY_LAYOUT and the chart function pass the
same key to update_layout() at the same time.
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st

from styles.theme import (
    BG, CARD, BORDER, GREEN, AMBER, RED, TEAL, WHITE, MUTED, TEXT_SEC,
    SEG_COLORS, PLOTLY_LAYOUT
)

# ── Default axis style applied separately to avoid duplicate-key crash ──
_XAXIS = dict(showgrid=False, linecolor=BORDER,
              tickfont=dict(color=TEXT_SEC), title_font=dict(color=TEXT_SEC))
_YAXIS = dict(showgrid=True, gridcolor=BORDER, zeroline=False,
              tickfont=dict(color=TEXT_SEC), title_font=dict(color=TEXT_SEC))
_LEGEND = dict(bgcolor="rgba(0,0,0,0)", font=dict(color=WHITE, size=11))


def _apply_theme(fig, height=360, legend_override=None,
                 xaxis_override=None, yaxis_override=None,
                 showlegend=True, **extra):
    """
    Two-step layout application.

    Step 1 applies the base tokens (font, colours, margin).
    Step 2 applies axes + legend in a separate call so there is no
    chance of a duplicate-keyword collision with caller-supplied keys.
    """
    # Step 1 — base tokens (no axes, no legend)
    fig.update_layout(**PLOTLY_LAYOUT, height=height, **extra)

    # Step 2 — axes and legend (separate call = no duplicate-key risk)
    xax = {**_XAXIS, **(xaxis_override or {})}
    yax = {**_YAXIS, **(yaxis_override or {})}
    leg = {**_LEGEND, **(legend_override or {})}
    fig.update_layout(
        xaxis=xax,
        yaxis=yax,
        legend=leg,
        showlegend=showlegend,
    )
    return fig


def _card(title, sub=""):
    s = f'<div class="card-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="card"><div class="card-title">{title}</div>{s}',
        unsafe_allow_html=True,
    )


def _end():
    st.markdown("</div>", unsafe_allow_html=True)


def _empty():
    st.info("No data available for the current filter selection.")


# ── Tab 1: Segmentation Overview ─────────────────────────────────────

def segment_donut(df):
    if df.empty:
        return _empty()
    counts = df["segment_name"].value_counts()
    fig = go.Figure(go.Pie(
        labels=counts.index,
        values=counts.values,
        hole=0.58,
        marker=dict(colors=[SEG_COLORS.get(s, TEAL) for s in counts.index]),
        textinfo="percent",
        textfont=dict(color="#111", size=12),
        hovertemplate="<b>%{label}</b><br>Buyers: %{value:,}<br>Share: %{percent}<extra></extra>",
    ))
    _apply_theme(
        fig, height=340,
        legend_override=dict(orientation="v", x=1.02, y=0.5,
                             font=dict(color=WHITE, size=11)),
    )
    st.plotly_chart(fig, use_container_width=True)


def segment_bar(df):
    if df.empty:
        return _empty()
    counts = df["segment_name"].value_counts().sort_values()
    fig = go.Figure(go.Bar(
        y=counts.index,
        x=counts.values,
        orientation="h",
        marker_color=[SEG_COLORS.get(s, TEAL) for s in counts.index],
        text=[f"{v:,}" for v in counts.values],
        textposition="outside",
        textfont=dict(color=WHITE, size=11),
        hovertemplate="<b>%{y}</b><br>Buyers: %{x:,}<extra></extra>",
    ))
    # Extra right margin prevents bar labels (e.g. "644") being clipped
    # at the chart edge when textposition="outside"
    fig.update_layout(margin=dict(l=12, r=80, t=36, b=12))
    _apply_theme(
        fig, height=340, showlegend=False,
        xaxis_override=dict(title="Number of Buyers"),
    )
    st.plotly_chart(fig, use_container_width=True)


def purpose_by_segment(df):
    if df.empty:
        return _empty()
    ct = pd.crosstab(df["segment_name"], df["acquisition_purpose"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    palette = {"Investment": AMBER, "Home": TEAL}
    fig = go.Figure()
    for col in ct_pct.columns:
        fig.add_trace(go.Bar(
            name=col,
            y=ct_pct.index,
            x=ct_pct[col],
            orientation="h",
            marker_color=palette.get(col, MUTED),
            text=[f"{v:.0f}%" for v in ct_pct[col]],
            textposition="inside",
            textfont=dict(color="#111", size=10),
            hovertemplate=f"<b>%{{y}}</b><br>{col}: %{{x:.1f}}%<extra></extra>",
        ))
    # xaxis_override sets range without conflicting with PLOTLY_LAYOUT
    _apply_theme(
        fig, height=340, barmode="stack",
        xaxis_override=dict(title="Percentage (%)", range=[0, 100]),
    )
    st.plotly_chart(fig, use_container_width=True)


def loan_by_segment(df):
    if df.empty:
        return _empty()
    ct = pd.crosstab(df["segment_name"], df["loan_applied"])
    ct_pct = ct.div(ct.sum(axis=1), axis=0) * 100
    palette = {"Yes": GREEN, "No": "#333333"}
    fig = go.Figure()
    for col in ct_pct.columns:
        fig.add_trace(go.Bar(
            name=f"Loan: {col}",
            y=ct_pct.index,
            x=ct_pct[col],
            orientation="h",
            marker_color=palette.get(col, MUTED),
            text=[f"{v:.0f}%" for v in ct_pct[col]],
            textposition="inside",
            textfont=dict(color=WHITE if col == "No" else "#111", size=10),
            hovertemplate=f"<b>%{{y}}</b><br>Loan {col}: %{{x:.1f}}%<extra></extra>",
        ))
    _apply_theme(
        fig, height=340, barmode="stack",
        xaxis_override=dict(title="Percentage (%)", range=[0, 100]),
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Tab 2: Investor Behaviour ─────────────────────────────────────────

def spend_by_segment(df):
    if df.empty:
        return _empty()
    g = df.groupby("segment_name")["total_spend"].mean().sort_values()
    fig = go.Figure(go.Bar(
        y=g.index,
        x=g.values / 1e6,
        orientation="h",
        marker_color=[SEG_COLORS.get(s, TEAL) for s in g.index],
        text=[f"${v/1e6:.2f}M" for v in g.values],
        textposition="outside",
        textfont=dict(color=WHITE, size=11),
        hovertemplate="<b>%{y}</b><br>Avg total spend: $%{x:.2f}M<extra></extra>",
    ))
    _apply_theme(
        fig, height=360, showlegend=False,
        xaxis_override=dict(title="Average Total Spend ($M)"),
    )
    st.plotly_chart(fig, use_container_width=True)


def price_vs_area_scatter(df):
    if df.empty:
        return _empty()
    sample = df.sample(min(2000, len(df)), random_state=42)
    fig = go.Figure()
    for seg, color in SEG_COLORS.items():
        sub = sample[sample["segment_name"] == seg]
        if sub.empty:
            continue
        fig.add_trace(go.Scattergl(
            x=sub["avg_area"],
            y=sub["avg_price"] / 1000,
            mode="markers",
            name=seg,
            marker=dict(color=color, size=6, opacity=0.65),
            hovertemplate=(
                f"<b>{seg}</b><br>"
                "Floor area: %{x:,.0f} sqft<br>"
                "Avg price: $%{y:.0f}K<extra></extra>"
            ),
        ))
    _apply_theme(
        fig, height=400,
        xaxis_override=dict(title="Average Floor Area (sqft)"),
        yaxis_override=dict(title="Average Price ($K)"),
        legend_override=dict(orientation="v", x=1.01, y=1,
                             font=dict(color=WHITE, size=10)),
    )
    st.plotly_chart(fig, use_container_width=True)


def units_by_segment(df):
    if df.empty:
        return _empty()
    g = df.groupby("segment_name")["total_units"].mean().sort_values()
    fig = go.Figure(go.Bar(
        y=g.index,
        x=g.values,
        orientation="h",
        marker_color=[SEG_COLORS.get(s, TEAL) for s in g.index],
        text=[f"{v:.1f}" for v in g.values],
        textposition="outside",
        textfont=dict(color=WHITE, size=11),
        hovertemplate="<b>%{y}</b><br>Avg units: %{x:.1f}<extra></extra>",
    ))
    _apply_theme(
        fig, height=340, showlegend=False,
        xaxis_override=dict(title="Average Units Purchased"),
    )
    st.plotly_chart(fig, use_container_width=True)


def satisfaction_segment(df):
    if df.empty:
        return _empty()
    g = df.groupby("segment_name")["satisfaction_score"].mean().sort_values(
        ascending=False)
    colors = [GREEN if v >= g.mean() else AMBER for v in g.values]
    fig = go.Figure(go.Bar(
        x=g.index,
        y=g.values,
        marker_color=colors,
        text=[f"{v:.2f}" for v in g.values],
        textposition="outside",
        textfont=dict(color=WHITE, size=11),
        hovertemplate="<b>%{x}</b><br>Avg satisfaction: %{y:.2f}/5<extra></extra>",
    ))
    _apply_theme(
        fig, height=340, showlegend=False,
        xaxis_override=dict(tickangle=-20),
        yaxis_override=dict(title="Avg Satisfaction Score", range=[0, 5.5]),
    )
    st.plotly_chart(fig, use_container_width=True)


def referral_channel(df):
    if df.empty:
        return _empty()
    g = (df.groupby(["referral_channel", "segment_name"])
           .size()
           .reset_index(name="count"))
    fig = px.bar(
        g, x="referral_channel", y="count", color="segment_name",
        color_discrete_map=SEG_COLORS, barmode="stack",
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{x}</b><br>Segment: %{fullData.name}<br>"
            "Buyers: %{y:,}<extra></extra>"
        )
    )
    _apply_theme(
        fig, height=340,
        xaxis_override=dict(title="Referral Channel"),
        yaxis_override=dict(title="Buyers"),
        legend_override=dict(title="Segment", orientation="v", x=1.01,
                             font=dict(color=WHITE, size=10)),
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Tab 3: Geographic Analysis ────────────────────────────────────────

def country_bar(df):
    if df.empty:
        return _empty()
    g = df.groupby("country")["client_id"].count().sort_values(ascending=False)
    colors = [GREEN if i == 0 else TEAL if i < 3 else MUTED
              for i in range(len(g))]
    fig = go.Figure(go.Bar(
        x=g.index,
        y=g.values,
        marker_color=colors,
        text=[f"{v:,}" for v in g.values],
        textposition="outside",
        textfont=dict(color=WHITE, size=11),
        hovertemplate="<b>%{x}</b><br>Buyers: %{y:,}<extra></extra>",
    ))
    _apply_theme(
        fig, height=340, showlegend=False,
        yaxis_override=dict(title="Number of Buyers"),
    )
    st.plotly_chart(fig, use_container_width=True)


def geo_segment_heatmap(df):
    if df.empty:
        return _empty()
    top_c = df["country"].value_counts().head(8).index
    pivot = df[df["country"].isin(top_c)].pivot_table(
        index="country", columns="segment_name",
        values="client_id", aggfunc="count", fill_value=0,
    )
    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=list(pivot.columns),
        y=list(pivot.index),
        colorscale=[[0, "#111111"], [0.5, TEAL], [1, AMBER]],
        text=[[str(v) if v > 0 else "" for v in row]
              for row in pivot.values],
        texttemplate="%{text}",
        textfont=dict(color=WHITE, size=11),
        hovertemplate="<b>%{y} — %{x}</b><br>Buyers: %{z}<extra></extra>",
        colorbar=dict(title="Buyers", tickfont=dict(color=WHITE)),
    ))
    _apply_theme(
        fig, height=360, showlegend=False,
        xaxis_override=dict(tickangle=-20),
    )
    st.plotly_chart(fig, use_container_width=True)


def spend_by_country(df):
    if df.empty:
        return _empty()
    g = (df.groupby("country")["total_spend"]
           .mean()
           .sort_values(ascending=False)
           .head(10))
    fig = go.Figure(go.Bar(
        x=g.index,
        y=g.values / 1e6,
        marker_color=TEAL,
        text=[f"${v/1e6:.2f}M" for v in g.values],
        textposition="outside",
        textfont=dict(color=WHITE, size=10),
        hovertemplate="<b>%{x}</b><br>Avg spend: $%{y:.2f}M<extra></extra>",
    ))
    _apply_theme(
        fig, height=340, showlegend=False,
        yaxis_override=dict(title="Avg Total Spend ($M)"),
    )
    st.plotly_chart(fig, use_container_width=True)


def age_by_segment(df):
    if df.empty:
        return _empty()
    fig = go.Figure()
    for seg, color in SEG_COLORS.items():
        sub = df[df["segment_name"] == seg]["age"]
        if sub.empty:
            continue
        fig.add_trace(go.Box(
            y=sub,
            name=seg,
            marker_color=color,
            boxmean=True,
            line_color=color,
            hovertemplate=f"<b>{seg}</b><br>Age: %{{y}}<extra></extra>",
        ))
    _apply_theme(
        fig, height=360, showlegend=False,
        yaxis_override=dict(title="Age"),
    )
    st.plotly_chart(fig, use_container_width=True)


# ── Tab 4: Segment Insights ───────────────────────────────────────────

def _hex_to_rgba(hex_color: str, alpha: float = 0.2) -> str:
    """Convert a #RRGGBB hex string to rgba(R,G,B,alpha).

    Plotly's Scatterpolar fillcolor does not accept 8-digit hex (#RRGGBBAA).
    It only accepts rgb/rgba strings, so we convert here instead of
    appending two hex digits to the colour string.
    """
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"


def segment_radar(df):
    """Spider/radar chart comparing normalised segment averages.

    Builds its own layout dict entirely (polar charts use a completely
    different layout structure from cartesian charts) so _apply_theme is
    not used here — there's no risk of axis/legend key conflicts because
    update_layout() is called only once with a fully-built dict.
    """
    if df.empty:
        return _empty()
    metrics = ["total_spend", "total_units", "avg_price",
               "avg_area", "satisfaction_score", "age"]
    labels  = ["Total Spend", "Units", "Avg Price",
               "Floor Area", "Satisfaction", "Age"]

    g = df.groupby("segment_name")[metrics].mean()
    # Normalise 0-1 so shape encodes relative strength, not absolute magnitude
    g_norm = (g - g.min()) / (g.max() - g.min() + 1e-9)

    fig = go.Figure()
    for seg in g_norm.index:
        vals = g_norm.loc[seg].tolist()
        vals += [vals[0]]   # close the polygon
        color = SEG_COLORS.get(seg, TEAL)
        fig.add_trace(go.Scatterpolar(
            r=vals,
            theta=labels + [labels[0]],
            fill="toself",
            name=seg,
            line=dict(color=color),
            fillcolor=_hex_to_rgba(color, alpha=0.2),  # rgba — Plotly rejects 8-digit hex
            hovertemplate=(
                f"<b>{seg}</b><br>%{{theta}}: %{{r:.2f}}<extra></extra>"
            ),
        ))

    fig.update_layout(
        polar=dict(
            bgcolor=CARD,
            radialaxis=dict(
                visible=True, range=[0, 1], color=MUTED,
                gridcolor=BORDER, tickfont=dict(color=MUTED, size=9),
            ),
            angularaxis=dict(
                color=WHITE, gridcolor=BORDER,
                tickfont=dict(color=WHITE, size=11),
            ),
        ),
        font=dict(family="Inter, sans-serif", color=WHITE, size=13),
        paper_bgcolor=CARD,
        plot_bgcolor=CARD,
        height=420,
        showlegend=True,
        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=WHITE, size=10),
            orientation="v",
            x=1.05,
            y=0.5,
        ),
        margin=dict(l=40, r=160, t=40, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
