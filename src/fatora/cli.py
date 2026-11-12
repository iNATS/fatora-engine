from decimal import Decimal

import typer
from fatora import __version__
from fatora.validation import validate_totals

app = typer.Typer(help="Fatora — open-source invoice and receipt extraction.")


@app.command()
def version() -> None:
    """Print the installed Fatora version."""
    typer.echo(f"Fatora {__version__}")


@app.command()
def validate_total(
    subtotal: str = typer.Option(..., help="Subtotal as a decimal string."),
    tax: str = typer.Option(..., help="Tax amount as a decimal string."),
    total: str = typer.Option(..., help="Reported total as a decimal string."),
) -> None:
    """Run a generic subtotal + tax = total arithmetic check."""
    result = validate_totals(Decimal(subtotal), Decimal(tax), Decimal(total))
    typer.echo(result)
