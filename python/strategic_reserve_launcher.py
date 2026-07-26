"""Dependency-light installed console launcher."""


def main() -> None:
    try:
        from ui.main import run
    except ModuleNotFoundError as exc:
        if exc.name == "tkinter":
            raise SystemExit(
                "Strategic Reserve needs a Python installation with Tk 8.6. "
                "Install your OS Tk package (often python3-tk) and retry."
            ) from None
        raise
    run()
