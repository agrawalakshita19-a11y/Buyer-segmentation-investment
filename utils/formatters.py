def fmt_currency(v):
    """Auto-scales: B above 1 billion, M above 1 million, K above 1 thousand.
    Keeps value and suffix on a single line — avoids the '$2520.75 M'
    line-break that occurs when Streamlit wraps a long string inside a
    narrow KPI card.
    """
    try:
        v = float(v)
    except (TypeError, ValueError):
        return "\u2014"
    if abs(v) >= 1_000_000_000:
        return f"${v/1_000_000_000:.2f}B"
    if abs(v) >= 1_000_000:
        return f"${v/1_000_000:.2f}M"
    if abs(v) >= 1_000:
        return f"${v/1_000:.1f}K"
    return f"${v:,.0f}"


def fmt_count(v):
    try:
        return f"{int(v):,}"
    except (TypeError, ValueError):
        return "\u2014"


def fmt_pct(v, decimals=1):
    try:
        return f"{float(v)*100:.{decimals}f}%"
    except (TypeError, ValueError):
        return "\u2014"


def fmt_num(v, decimals=1):
    try:
        return f"{float(v):,.{decimals}f}"
    except (TypeError, ValueError):
        return "\u2014"
