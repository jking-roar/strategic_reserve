"""Installed launcher diagnostics do not require Tk to be importable."""

import builtins

import pytest

from strategic_reserve_launcher import main


def test_launcher_reports_missing_tk_without_import_traceback(monkeypatch) -> None:
    original = builtins.__import__

    def importing(name, *args, **kwargs):
        if name == "ui.main":
            error = ModuleNotFoundError("No module named tkinter")
            error.name = "tkinter"
            raise error
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", importing)
    with pytest.raises(SystemExit, match="Python installation with Tk 8.6"):
        main()
