from rich.table import Table
import rich


def safe_faker_method(faker_instance, method_name, *args):
    """Safely get the Faker method by name and execute it with arguments."""
    if hasattr(faker_instance, method_name):
        method = getattr(faker_instance, method_name)
        return method(*args)
    else:
        raise ValueError(f"No such Faker method: {method_name}")


def print_df_as_table(df, title="Data Sample"):
    table = Table(
        show_header=True,
        title=title,
        header_style="bold magenta",
        expand=True,
        show_lines=True,
    )
    table.border_style = "yellow"
    for column in df.columns:
        table.add_column(column)

    # Add rows to the table
    for index, row in df.head(3).iterrows():
        # Convert each row to string format, necessary to handle different data types
        table.add_row(*[str(item) for item in row.values])
    rich.print(table)
