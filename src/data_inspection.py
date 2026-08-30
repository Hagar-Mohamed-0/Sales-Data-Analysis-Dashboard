import pandas as pd
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()


def inspect_data(df: pd.DataFrame) -> None:
    """Display a visual inspection of a DataFrame in the CLI."""

    # DATASET OVERVIEW

    console.print(
        Panel.fit(
            "[bold cyan]DATASET INSPECTION[/bold cyan]",
            border_style="cyan"
        )
    )

    overview = Table(title="Dataset Overview")

    overview.add_column("Property", style="cyan")
    overview.add_column("Value", style="green")

    overview.add_row("Rows", f"{df.shape[0]:,}")
    overview.add_row("Columns", f"{df.shape[1]:,}")

    # ---------------------------------------------------------
    # Duplicate business records
    # ---------------------------------------------------------

    duplicate_columns = ["order_id", "product_id"]

    existing_columns = [
        column
        for column in duplicate_columns
        if column in df.columns
    ]

    if len(existing_columns) == len(duplicate_columns):
        duplicate_count = df.duplicated(
            subset=existing_columns,
            keep=False
        ).sum()

        overview.add_row(
            "Duplicate Records",
            f"{duplicate_count:,}"
        )
    else:
        overview.add_row(
            "Duplicate Records",
            "[yellow]Not checked[/yellow]"
        )

    console.print(overview)

    # COLUMNS

    columns = Table(title="Columns")

    columns.add_column("#", style="dim")
    columns.add_column("Column Name", style="cyan")
    columns.add_column("Data Type", style="yellow")

    for index, column in enumerate(df.columns, start=1):
        columns.add_row(
            str(index),
            str(column),
            str(df[column].dtype)
        )

    console.print(columns)

    # FIRST 5 ROWS

    console.print(
        Panel(
            df.head().to_string(index=False),
            title="First 5 Rows",
            border_style="green"
        )
    )

    # MISSING VALUES

    missing = Table(title="Missing Values")

    missing.add_column("Column", style="cyan")
    missing.add_column("Missing", style="yellow")
    missing.add_column("Status")

    missing_counts = df.isna().sum()

    for column, count in missing_counts.items():

        if count == 0:
            status = "[green]✓ Clean[/green]"
        else:
            status = "[red]⚠ Missing[/red]"

        missing.add_row(
            str(column),
            f"{count:,}",
            status
        )

    console.print(missing)

    #SUMMARY STATISTICS

    console.print(
        Panel(
            df.describe(include="all").to_string(),
            title="Summary Statistics",
            border_style="magenta"
        )
    )