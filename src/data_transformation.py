import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transform cleaned data into an analysis-ready DataFrame.
    """

    df = df.copy()

    # DATE FEATURES

    if "order_date" in df.columns:

        df["order_year"] = df["order_date"].dt.year
        df["order_month"] = df["order_date"].dt.month
        df["order_month_name"] = df["order_date"].dt.month_name()
        df["order_quarter"] = df["order_date"].dt.quarter

    # SHIPPING FEATURES

    if "shipping_days" in df.columns:

        df["shipping_category"] = pd.cut(
            df["shipping_days"],
            bins=[-1, 2, 5, float("inf")],
            labels=[
                "Fast",
                "Standard",
                "Slow",
            ],
        )

    # PROFITABILITY

    if "profit_margin" in df.columns:

        df["profit_status"] = df["profit_margin"].apply(
            lambda x: (
                "Loss"
                if x < 0
                else "Low Margin"
                if x < 0.10
                else "Healthy Margin"
            )
        )

    return df