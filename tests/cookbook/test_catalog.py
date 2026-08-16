import importlib.util
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("cookbook_runner", HERE / "runner.py")
assert SPEC and SPEC.loader
runner = importlib.util.module_from_spec(SPEC)
sys.path.insert(0, str(HERE))
SPEC.loader.exec_module(runner)


def test_every_cookbook_has_a_valid_contract():
    catalog = runner.load_catalog()
    runner.validate_catalog(catalog)
    assert set(catalog) == runner.discover_projects()


def test_python_sources_compile():
    for project in sorted(runner.discover_projects()):
        if not project.startswith("python-"):
            continue
        for source in (runner.COOKBOOK / project).rglob("*.py"):
            compile(source.read_text(encoding="utf-8"), str(source), "exec")


def test_catalog_is_stably_sorted():
    raw = json.loads(runner.CATALOG_PATH.read_text(encoding="utf-8"))
    names = list(raw["projects"])
    assert names == sorted(names)
