"""
Sidebar filters.

Dark sidebar with border separation matches Parcl's terminal-style UI.
"""
import streamlit as st


def render_filters(df):
    st.sidebar.markdown(
        '<div class="sidebar-brand">parcl<span>.</span></div>'
        '<div class="sidebar-caption">Buyer Intelligence Platform</div>',
        unsafe_allow_html=True,
    )
    st.sidebar.divider()

    if df.empty:
        st.sidebar.warning("No data loaded.")
        return df

    st.sidebar.markdown('<div class="filter-head">Country</div>', unsafe_allow_html=True)
    countries = sorted(df["country"].dropna().unique())
    sel_country = st.sidebar.multiselect("Country", countries, default=countries,
                                          key="country", label_visibility="collapsed")

    st.sidebar.markdown('<div class="filter-head">Region</div>', unsafe_allow_html=True)
    regions = sorted(df[df["country"].isin(sel_country)]["region"].dropna().unique())
    sel_region = st.sidebar.multiselect("Region", regions, default=regions,
                                         key="region", label_visibility="collapsed")

    st.sidebar.markdown('<div class="filter-head">Acquisition Purpose</div>', unsafe_allow_html=True)
    purposes = sorted(df["acquisition_purpose"].dropna().unique())
    sel_purpose = st.sidebar.multiselect("Acquisition Purpose", purposes, default=purposes,
                                          key="purpose", label_visibility="collapsed")

    st.sidebar.markdown('<div class="filter-head">Client Type</div>', unsafe_allow_html=True)
    ctypes = sorted(df["client_type"].dropna().unique())
    sel_ctype = st.sidebar.multiselect("Client Type", ctypes, default=ctypes,
                                        key="ctype", label_visibility="collapsed")

    st.sidebar.markdown('<div class="filter-head">Buyer Segment</div>', unsafe_allow_html=True)
    segments = sorted(df["segment_name"].dropna().unique())
    sel_seg = st.sidebar.multiselect("Buyer Segment", segments, default=segments,
                                      key="segment", label_visibility="collapsed")

    filtered = df[
        df["country"].isin(sel_country) &
        df["region"].isin(sel_region) &
        df["acquisition_purpose"].isin(sel_purpose) &
        df["client_type"].isin(sel_ctype) &
        df["segment_name"].isin(sel_seg)
    ]

    st.sidebar.divider()
    st.sidebar.markdown(
        f'<div style="font-size:0.75rem;color:#888;">'
        f'<span style="color:#00D97E;font-weight:700;">{len(filtered):,}</span>'
        f' buyers in selection</div>',
        unsafe_allow_html=True,
    )
    return filtered
