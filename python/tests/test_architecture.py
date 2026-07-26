from pathlib import Path
import ast


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
    root = Path(__file__).resolve().parents[1]
    for file in (root / "ai").glob("*.py"):
        source = file.read_text(encoding="utf-8")
        assert "import ui" not in source
        assert "from ui" not in source


def test_python_modules_follow_engine_ai_ui_dependency_direction() -> None:
    root = Path(__file__).resolve().parents[1]
    layer = {"game_engine": 0, "ai": 1, "ui": 2}
    for package, package_level in layer.items():
        for file in (root / package).glob("*.py"):
            tree = ast.parse(file.read_text(encoding="utf-8"))
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[0])
            forbidden = {name for name, level in layer.items() if level > package_level}
            assert imported.isdisjoint(forbidden), f"{file} imports a higher layer"
