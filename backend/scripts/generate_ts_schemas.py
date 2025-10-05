#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from app.main import create_application

OUTPUT = Path(__file__).resolve().parents[2] / "frontend" / "schema" / "openapi.json"


def generate() -> None:
    app = create_application()
    openapi_schema = app.openapi()

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(openapi_schema, indent=2))
    print(f"OpenAPI schema exported to {OUTPUT}")


if __name__ == "__main__":
    generate()
