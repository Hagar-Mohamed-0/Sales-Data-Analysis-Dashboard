import numpy as np
import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize DataFrame column names."""

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^\w\s-]", "", regex=True)
        .str.replace(r"[\s-]+", "_", regex=True)
        .str.strip("_")
    )

    return df


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove unnecessary whitespace and handle empty text values."""

    text_columns = df.select_dtypes(include="object").columns

    for col in text_columns:
        df[col] = df[col].astype("string").str.strip()
        df[col] = df[col].replace("", pd.NA)

    return df


def fix_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert columns to appropriate data types."""

    date_columns = [
        "order_date",
        "ship_date",
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
            )

    numeric_columns = [
        "sales",
        "quantity",
        "discount",
        "profit",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce",
            )

    return df


def validate_values(df: pd.DataFrame) -> pd.DataFrame:
    """Replace invalid or impossible values with missing values."""

    # Quantity cannot be negative
    if "quantity" in df.columns:
        df.loc[df["quantity"] < 0, "quantity"] = np.nan

    # Discount must be between 0 and 1
    if "discount" in df.columns:
        invalid_discount = ~df["discount"].between(0, 1)
        df.loc[invalid_discount, "discount"] = np.nan

    # Sales should not be negative
    if "sales" in df.columns:
        df.loc[df["sales"] < 0, "sales"] = np.nan

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Handle missing values based on column type."""

    categorical_columns = [
        "customer_name",
        "segment",
        "country",
        "city",
        "state",
        "region",
        "category",
        "sub_category",
    ]

    for col in categorical_columns:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    numeric_columns = [
        "sales",
        "quantity",
        "discount",
        "profit",
    ]

    for col in numeric_columns:
        if col in df.columns and df[col].notna().any():
            df[col] = df[col].fillna(df[col].median())

    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detect and handle duplicate records.

    1. Exact duplicates:
       All columns are identical except row_id.

    2. Business duplicates:
       Same order_id + product_id.
    """

    #1. EXACT DUPLICATES

    if "row_id" in df.columns:

        comparison_columns = [
            column
            for column in df.columns
            if column != "row_id"
        ]

        exact_duplicates = df.duplicated(
            subset=comparison_columns,
            keep="first"
        )

        exact_count = exact_duplicates.sum()

        df = df.loc[~exact_duplicates].copy()

    else:
        exact_count = 0

    #2.BUSINESS DUPLICATES

    business_columns = [
        "order_id",
        "product_id"
    ]

    if all(column in df.columns for column in business_columns):

        business_duplicates = df.duplicated(
            subset=business_columns,
            keep="first"
        )

        business_count = business_duplicates.sum()

        # Keep the first occurrence
        df = df.loc[~business_duplicates].copy()

    else:
        business_count = 0

    
    #REPORT
    
    print(f"Exact duplicates removed: {exact_count:,}")
    print(f"Business duplicates removed: {business_count:,}")

    return df

def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add useful columns for analysis."""

    # Profit margin
    if "profit" in df.columns and "sales" in df.columns:
        df["profit_margin"] = np.where(
            df["sales"] != 0,
            df["profit"] / df["sales"],
            0,
        )

    # Shipping duration
    if "order_date" in df.columns and "ship_date" in df.columns:
        df["shipping_days"] = (
            df["ship_date"] - df["order_date"]
        ).dt.days

    return df


def clean_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """
    Execute the complete data-cleaning pipeline.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """

    df = df.copy()

    # 1. Standardize column names
    df = standardize_column_names(df)

    # 2. Clean text values
    df = clean_text_columns(df)

    # 3. Fix data types
    df = fix_data_types(df)

    # 4. Validate values
    df = validate_values(df)

    # 5. Handle missing values
    df = handle_missing_values(df)

    # 6. Remove duplicates
    df = remove_duplicates(df)

    # 7. Add derived columns
    df = add_derived_columns(df)

    return df