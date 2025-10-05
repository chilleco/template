"""Generate OpenAPI schema and sync to frontend."""

from __future__ import annotations

import json
from pathlib import Path

import typer

from backend.app.main import create_application

app = typer.Typer(help="Export OpenAPI spec and TypeScript helpers")


@app.command()
def openapi(out: Path = Path("docs/openapi.json")) -> None:
    application = create_application()
    schema = application.openapi()
    out.write_text(json.dumps(schema, indent=2))
    typer.echo(f"OpenAPI schema written to {out}")


if __name__ == "__main__":
    app()
