import pandas as pd
import plotly.express as px


# ============================================================
# COLOR PALETTES
# ============================================================

CATEGORY_COLORS = {
    "Technology": "#3498DB",
    "Furniture": "#2ECC71",
    "Office Supplies": "#F1C40F",
}


REGION_COLORS = {
    "West": "#E67E22",
    "East": "#9B59B6",
    "Central": "#1ABC9C",
    "South": "#E74C3C",
}


SEGMENT_COLORS = {
    "Consumer": "#3498DB",
    "Corporate": "#9B59B6",
    "Home Office": "#2ECC71",
}


# ============================================================
# COMMON CHART STYLE
# ============================================================

def style_chart(fig):
    """
    Apply a consistent style to all dashboard charts.
    """

    fig.update_layout(
        height=350,
        margin=dict(
            l=20,
            r=20,
            t=55,
            b=20,
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(
            family="Arial",
            size=12,
            color="#1F2937",
        ),
    )

    return fig


# ============================================================
# SALES BY CATEGORY
# ============================================================

def sales_by_category(df: pd.DataFrame):
    """
    Display total sales by product category.
    """

    data = (
        df.groupby("category", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.bar(
        data,
        x="category",
        y="sales",
        color="category",
        title="Sales by Category",
        text_auto=".2s",
        color_discrete_map=CATEGORY_COLORS,
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Sales",
    )

    return style_chart(fig)


# ============================================================
# SALES BY REGION
# ============================================================

def sales_by_region(df: pd.DataFrame):
    """
    Display total sales by region.
    """

    data = (
        df.groupby("region", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.bar(
        data,
        x="region",
        y="sales",
        color="region",
        title="Sales by Region",
        text_auto=".2s",
        color_discrete_map=REGION_COLORS,
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Sales",
    )

    return style_chart(fig)


# ============================================================
# SALES OVER TIME
# ============================================================

def sales_over_time(df: pd.DataFrame):
    """
    Display sales across time.
    """

    # Prefer the transformed month column
    if "order_month_name" in df.columns:

        data = (
            df.groupby(
                ["order_year", "order_month", "order_month_name"],
                as_index=False,
            )["sales"]
            .sum()
            .sort_values(
                ["order_year", "order_month"]
            )
        )

        data["period"] = (
            data["order_month_name"]
            + " "
            + data["order_year"].astype(str)
        )

        fig = px.line(
            data,
            x="period",
            y="sales",
            title="Sales Over Time",
            markers=True,
        )

    else:

        # Fallback if transformation did not create date features
        data = (
            df.groupby("order_date", as_index=False)["sales"]
            .sum()
            .sort_values("order_date")
        )

        fig = px.line(
            data,
            x="order_date",
            y="sales",
            title="Sales Over Time",
            markers=True,
        )

    fig.update_traces(
        line_width=3,
    )

    fig.update_layout(
        xaxis_title=None,
        yaxis_title="Sales",
    )

    return style_chart(fig)


# ============================================================
# SALES BY SEGMENT
# ============================================================

def sales_by_segment(df: pd.DataFrame):
    """
    Display total sales by customer segment.
    """

    data = (
        df.groupby("segment", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    fig = px.pie(
        data,
        names="segment",
        values="sales",
        title="Sales by Customer Segment",
        hole=0.45,
        color="segment",
        color_discrete_map=SEGMENT_COLORS,
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
    )

    return style_chart(fig)


# ============================================================
# PROFIT BY CATEGORY
# ============================================================

def profit_by_category(df: pd.DataFrame):
    """
    Display total profit by product category.
    """

    data = (
        df.groupby("category", as_index=False)["profit"]
        .sum()
        .sort_values("profit", ascending=False)
    )

    fig = px.bar(
        data,
        x="category",
        y="profit",
        color="category",
        title="Profit by Category",
        text_auto=".2s",
        color_discrete_map=CATEGORY_COLORS,
    )

    fig.update_layout(
        showlegend=False,
        xaxis_title=None,
        yaxis_title="Profit",
    )

    return style_chart(fig)
