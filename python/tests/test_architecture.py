from pathlib import Path


def test_layer_imports_are_valid() -> None:
    import game_engine  # noqa: F401
    import ai  # noqa: F401
    import ui  # noqa: F401


def test_game_engine_has_no_reverse_dependencies() -> None:
    root = Path(__file__).resolve().parents[1]
    for file in (root / "game_engine").glob("*.py"):
        source = file.read_text(encoding="utf-8")
        assert "import ai" not in source
        assert "from ai" not in source
        assert "import ui" not in source
        assert "from ui" not in source


def test_ai_has_no_ui_dependency() -> None:
    source = (Path(__file__).resolve().parents[1] / "ai" / "__init__.py").read_text(
        encoding="utf-8"
    )
    assert "import ui" not in source
    assert "from ui" not in source

