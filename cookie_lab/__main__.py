"""CLI entry point for running the Cookie Lab app."""

from __future__ import annotations

from .app import create_app


def main() -> None:
    """Run the development server for local Cookie Lab use."""
    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)


if __name__ == "__main__":
    main()
