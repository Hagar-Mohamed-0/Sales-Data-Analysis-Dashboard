
import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================
# IMPORTS
# ============================================================

from src.data_loader import load_data
from src.data_cleaning import clean_pipeline
from src.data_transformation import transform_data

from dashboard.charts import (
    sales_by_category,
    sales_by_region,
    sales_over_time,
    sales_by_segment,
    profit_by_category,
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #F7F9FC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Header */

    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1F2937;
        margin-bottom: 0;
    }

    .subtitle {
        color: #6B7280;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    /* Metric cards */

    div[data-testid="stMetric"] {
        background-color: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #6B7280;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        color: #111827;
        font-size: 28px;
        font-weight: 700;
    }

    /* Chart cards */

    .chart-container {
        background-color: white;
        border-radius: 14px;
        border: 1px solid #E5E7EB;
        padding: 10px;
        margin-bottom: 15px;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.04);
    }

    /* Sidebar */

    section[data-testid="stSidebar"] {
        background-color: white;
        border-right: 1px solid #E5E7EB;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# DATA PATH
# ============================================================

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "Sample - Superstore.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def get_data():

    df = load_data(DATA_PATH)

    df = clean_pipeline(df)

    df = transform_data(df)

    return df


try:

    df = get_data()

except Exception as error:

    st.error(
        f"Unable to load the dataset: {error}"
    )

    st.stop()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📊 Sales Analytics</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    'Superstore business performance dashboard'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

required_columns = [
    "category",
    "region",
    "segment",
    "sales",
    "profit",
    "order_id",
    "customer_id",
]


missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]


if missing_columns:

    st.error(
        "The following required columns are missing:"
    )

    st.code(
        ", ".join(missing_columns)
    )

    st.write("Available columns:")

    st.code(
        ", ".join(df.columns.tolist())
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔎 Dashboard Filters")

st.sidebar.write(
    "Use the filters below to explore the dataset."
)

st.sidebar.divider()


# ============================================================
# CATEGORY
# ============================================================

categories = sorted(
    df["category"]
    .dropna()
    .unique()
)

selected_categories = st.sidebar.multiselect(
    "Category",
    categories,
    default=categories,
)


# ============================================================
# REGION
# ============================================================

regions = sorted(
    df["region"]
    .dropna()
    .unique()
)

selected_regions = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions,
)


# ============================================================
# SEGMENT
# ============================================================

segments = sorted(
    df["segment"]
    .dropna()
    .unique()
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments,
)


# ============================================================
# YEAR
# ============================================================

if "order_year" in df.columns:

    years = sorted(
        df["order_year"]
        .dropna()
        .unique()
    )

    selected_years = st.sidebar.multiselect(
        "Year",
        years,
        default=years,
    )

else:

    selected_years = []


# ============================================================
# FILTER DATA
# ============================================================

filtered_df = df.copy()


if selected_categories:

    filtered_df = filtered_df[
        filtered_df["category"].isin(
            selected_categories
        )
    ]


if selected_regions:

    filtered_df = filtered_df[
        filtered_df["region"].isin(
            selected_regions
        )
    ]


if selected_segments:

    filtered_df = filtered_df[
        filtered_df["segment"].isin(
            selected_segments
        )
    ]


if selected_years:

    filtered_df = filtered_df[
        filtered_df["order_year"].isin(
            selected_years
        )
    ]


# ============================================================
# EMPTY DATA CHECK
# ============================================================

if filtered_df.empty:

    st.warning(
        "No data matches the selected filters."
    )

    st.stop()


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_sales = filtered_df["sales"].sum()

total_profit = filtered_df["profit"].sum()

total_orders = filtered_df["order_id"].nunique()

total_customers = filtered_df["customer_id"].nunique()


# ============================================================
# KPI SECTION
# ============================================================

st.subheader("📈 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        label="💰 Total Sales",
        value=f"${total_sales:,.0f}",
    )


with col2:

    st.metric(
        label="📈 Total Profit",
        value=f"${total_profit:,.0f}",
    )


with col3:

    st.metric(
        label="🛒 Total Orders",
        value=f"{total_orders:,}",
    )


with col4:

    st.metric(
        label="👥 Customers",
        value=f"{total_customers:,}",
    )


st.markdown("<br>", unsafe_allow_html=True)


# ============================================================
# CHART ROW 1
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        sales_by_category(filtered_df),
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        sales_by_region(filtered_df),
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# CHART ROW 2
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        sales_over_time(filtered_df),
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


with col2:

    st.markdown(
        '<div class="chart-container">',
        unsafe_allow_html=True,
    )

    st.plotly_chart(
        sales_by_segment(filtered_df),
        use_container_width=True,
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True,
    )


# ============================================================
# PROFIT CHART
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    '<div class="chart-container">',
    unsafe_allow_html=True,
)

st.plotly_chart(
    profit_by_category(filtered_df),
    use_container_width=True,
)

st.markdown(
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# FILTERED DATA
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("📋 Filtered Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True,
    height=350,
    hide_index=True,
)
