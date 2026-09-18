"""
KPI cards.

Three-row layout: primary headline metrics first, then segment-level
detail, then property market summary. Per-metric accent bars use the
colour vocabulary: green = scale/volume, amber = financial, red = risk,
teal = engagement.
"""
import streamlit as st
from utils.formatters import fmt_currency, fmt_count, fmt_num
from styles.theme import GREEN, AMBER, RED, TEAL, SEG_COLORS


def _kpi(label, value, sub, accent):
    st.markdown(f"""
    <div class="kpi">
        <div class="kpi-bar" style="background:{accent};"></div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-val">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)


def render_kpis(df, props_df=None):
    if df.empty:
        st.info("No buyers match the current filter selection.")
        return

    total      = len(df)
    invest_pct = (df["acquisition_purpose"] == "Investment").mean() * 100
    avg_spend  = df["total_spend"].mean()
    total_rev  = df["total_spend"].sum()
    loan_pct   = (df["loan_applied"] == "Yes").mean() * 100
    avg_units  = df["total_units"].mean()
    avg_sat    = df["satisfaction_score"].mean()
    corp_pct   = (df["client_type"] == "Company").mean() * 100

    # Dominant segment
    top_seg    = df["segment_name"].value_counts().idxmax()
    top_seg_n  = df["segment_name"].value_counts().max()

    c1, c2, c3, c4 = st.columns([1.5, 1, 1, 1])
    with c1:
        _kpi("Total Buyers Analysed", fmt_count(total),
             f"across {df['country'].nunique()} countries · {df['region'].nunique()} regions", GREEN)
    with c2:
        _kpi("Portfolio Value", fmt_currency(total_rev),
             f"avg {fmt_currency(avg_spend)} per buyer", AMBER)
    with c3:
        _kpi("Investment Purpose", f"{invest_pct:.1f}%",
             f"{fmt_count(int(df['acquisition_purpose'].eq('Investment').sum()))} investment buyers", RED)
    with c4:
        _kpi("Loan Applied Rate", f"{loan_pct:.1f}%",
             f"{fmt_count(int(df['loan_applied'].eq('Yes').sum()))} buyers used financing", TEAL)

    st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

    e1, e2, e3 = st.columns(3)
    with e1:
        _kpi("Avg Units per Buyer", fmt_num(avg_units),
             f"portfolio investor avg: {fmt_num(df[df['segment_name']=='Portfolio Investors']['total_units'].mean())}", AMBER)
    with e2:
        _kpi("Avg Satisfaction", f"{avg_sat:.2f} / 5",
             f"based on {fmt_count(total)} satisfaction responses", GREEN)
    with e3:
        _kpi("Dominant Segment", top_seg,
             f"{fmt_count(top_seg_n)} buyers · {top_seg_n/total*100:.1f}% of selection",
             SEG_COLORS.get(top_seg, TEAL))
