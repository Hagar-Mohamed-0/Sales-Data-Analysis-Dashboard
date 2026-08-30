import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate the main sales performance KPIs."""

    kpis = {}

    if "sales" in df.columns:
        kpis["total_sales"] = df["sales"].sum()

    if "profit" in df.columns:
        kpis["total_profit"] = df["profit"].sum()

    if "order_id" in df.columns:
        kpis["total_orders"] = df["order_id"].nunique()

    if "customer_id" in df.columns:
        kpis["total_customers"] = df["customer_id"].nunique()

    if "sales" in df.columns and "order_id" in df.columns:
        total_orders = df["order_id"].nunique()

        if total_orders > 0:
            kpis["average_order_value"] = (
                df["sales"].sum() / total_orders
            )

    if "profit_margin" in df.columns:
        kpis["average_profit_margin"] = (
            df["profit_margin"].mean()
        )

    return kpis


def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales and profit by region."""

    required_columns = [
        "region",
        "sales",
        "profit",
    ]

    if not all(column in df.columns for column in required_columns):
        return pd.DataFrame()

    return (
        df.groupby("region", as_index=False)
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values("sales", ascending=False)
    )


def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales and profit by product category."""

    required_columns = [
        "category",
        "sales",
        "profit",
    ]

    if not all(column in df.columns for column in required_columns):
        return pd.DataFrame()

    return (
        df.groupby("category", as_index=False)
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values("sales", ascending=False)
    )


def sales_by_segment(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate sales and profit by customer segment."""

    required_columns = [
        "segment",
        "sales",
        "profit",
    ]

    if not all(column in df.columns for column in required_columns):
        return pd.DataFrame()

    return (
        df.groupby("segment", as_index=False)
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values("sales", ascending=False)
    )


def top_products(
    df: pd.DataFrame,
    n: int = 10,
) -> pd.DataFrame:
    """Return the top products by sales."""

    required_columns = [
        "product_name",
        "sales",
        "profit",
    ]

    if not all(column in df.columns for column in required_columns):
        return pd.DataFrame()

    return (
        df.groupby("product_name", as_index=False)
        .agg(
            sales=("sales", "sum"),
            profit=("profit", "sum"),
        )
        .sort_values("sales", ascending=False)
        .head(n)
    )


def analyze_data(df: pd.DataFrame) -> dict:
    """Run the complete analysis pipeline."""

    results = {
        "kpis": calculate_kpis(df),
        "sales_by_region": sales_by_region(df),
        "sales_by_category": sales_by_category(df),
        "sales_by_segment": sales_by_segment(df),
        "top_products": top_products(df),
    }

    return results