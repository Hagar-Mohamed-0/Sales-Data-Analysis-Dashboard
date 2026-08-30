from pathlib import Path

from rich.console import Console
from rich.table import Table

from src.data_loader import load_data
from src.data_inspection import inspect_data
from src.data_cleaning import clean_pipeline
from src.data_transformation import transform_data
from src.data_analysis import analyze_data


console = Console()

PROJECT_PATH = Path(__file__).resolve().parent


def display_kpis(kpis: dict) -> None:
    """Display KPI results in the CLI."""

    table = Table(title="Sales Performance KPIs")

    table.add_column("KPI", style="cyan")
    table.add_column("Value", style="green")

    for name, value in kpis.items():

        if "margin" in name.lower():
            formatted_value = f"{value:.2%}"

        elif isinstance(value, float):
            formatted_value = f"{value:,.2f}"

        else:
            formatted_value = f"{value:,}"

        table.add_row(
            name.replace("_", " ").title(),
            formatted_value,
        )

    console.print(table)


def main() -> None:

    # =========================================================
    # LOAD
    # =========================================================

    data_path = (
        PROJECT_PATH
        / "data"
        / "raw"
        / "Sample - Superstore.csv"
    )

    df = load_data(data_path)

    # =========================================================
    # RAW DATA
    # =========================================================

    console.print()
    console.rule("[bold cyan]RAW DATA[/bold cyan]")
    console.print()

    inspect_data(df)

    # =========================================================
    # CLEAN
    # =========================================================

    df = clean_pipeline(df)

    # =========================================================
    # CLEANED DATA
    # =========================================================

    console.print("\n\n")
    console.rule("[bold green]CLEANED DATA[/bold green]")
    console.print()

    inspect_data(df)

    # =========================================================
    # TRANSFORM
    # =========================================================

    df = transform_data(df)

    # =========================================================
    # TRANSFORMED DATA
    # =========================================================

    console.print("\n\n")
    console.rule("[bold yellow]TRANSFORMED DATA[/bold yellow]")
    console.print()

    inspect_data(df)

    # =========================================================
    # ANALYSIS
    # =========================================================

    results = analyze_data(df)

    console.print("\n\n")
    console.rule("[bold magenta]DATA ANALYSIS[/bold magenta]")
    console.print()

    # =========================================================
    # KPIs
    # =========================================================

    display_kpis(results["kpis"])

    # =========================================================
    # SALES BY REGION
    # =========================================================

    console.print()
    console.print(
        results["sales_by_region"].to_string(index=False)
    )

    # =========================================================
    # SALES BY CATEGORY
    # =========================================================

    console.print()
    console.print(
        results["sales_by_category"].to_string(index=False)
    )

    # =========================================================
    # SALES BY SEGMENT
    # =========================================================

    console.print()
    console.print(
        results["sales_by_segment"].to_string(index=False)
    )

    # =========================================================
    # TOP PRODUCTS
    # =========================================================

    console.print()
    console.print(
        results["top_products"].to_string(index=False)
    )


if __name__ == "__main__":
    main()