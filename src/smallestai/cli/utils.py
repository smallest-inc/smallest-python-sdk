import ast
import fnmatch
import io
import zipfile
from pathlib import Path
from typing import List, Set

from loguru import logger
from rich.console import Console

console = Console()


def find_required_env_vars(directory: Path) -> Set[str]:
    """Walk every `.py` file under `directory` and return the set of env var
    names the user's code reads via `os.getenv("X")` / `os.environ["X"]` /
    `os.environ.get("X", ...)`.

    Used by the deploy command to warn the customer about env vars they
    reference but which the platform won't provide. Doesn't detect dynamic
    names (e.g. `os.getenv(some_var)`) — those would need runtime reflection.
    """
    found: Set[str] = set()

    for py_file in directory.rglob("*.py"):
        if any(part in {"__pycache__", ".venv", "venv", ".git"} for part in py_file.parts):
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except (SyntaxError, UnicodeDecodeError):
            continue

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            # os.getenv("X") / os.environ.get("X", ...)
            if (
                isinstance(node.func, ast.Attribute)
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                attr = node.func.attr
                if attr == "getenv":
                    # os.getenv("X")
                    if isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                        found.add(node.args[0].value)
                elif attr == "get":
                    # os.environ.get("X", ...)
                    parent = node.func.value
                    if (
                        isinstance(parent, ast.Attribute)
                        and parent.attr == "environ"
                        and isinstance(parent.value, ast.Name)
                        and parent.value.id == "os"
                    ):
                        found.add(node.args[0].value)

        # os.environ["X"] — Subscript form
        for node in ast.walk(tree):
            if not isinstance(node, ast.Subscript):
                continue
            if (
                isinstance(node.value, ast.Attribute)
                and node.value.attr == "environ"
                and isinstance(node.value.value, ast.Name)
                and node.value.value.id == "os"
            ):
                key = node.slice
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    found.add(key.value)

    return found


def create_zip_from_directory(directory: Path):
    """Create a zip file from a directory, excluding files based on .gitignore patterns."""

    excluded_patterns = {
        # Byte-compiled / optimized / DLL files
        "__pycache__",
        "*.py[codz]",
        "*$py.class",
        "*.so",
        # Distribution / packaging
        ".Python",
        "build",
        "develop-eggs",
        "dist",
        "downloads",
        "eggs",
        ".eggs",
        "lib",
        "lib64",
        "parts",
        "sdist",
        "var",
        "wheels",
        "share",
        "*.egg-info",
        ".installed.cfg",
        "*.egg",
        "MANIFEST",
        # PyInstaller
        "*.manifest",
        "*.spec",
        # Installer logs
        "pip-log.txt",
        "pip-delete-this-directory.txt",
        # Unit test / coverage reports
        "htmlcov",
        ".tox",
        ".nox",
        ".coverage",
        ".coverage.*",
        ".cache",
        "nosetests.xml",
        "coverage.xml",
        "*.cover",
        "*.py.cover",
        ".hypothesis",
        ".pytest_cache",
        "cover",
        # Translations
        "*.mo",
        "*.pot",
        # Django
        "*.log",
        "local_settings.py",
        "db.sqlite3",
        "db.sqlite3-journal",
        # Flask
        "instance",
        ".webassets-cache",
        # Scrapy
        ".scrapy",
        # Sphinx documentation
        "docs/_build",
        # PyBuilder
        ".pybuilder",
        "target",
        # Jupyter Notebook
        ".ipynb_checkpoints",
        # IPython
        "profile_default",
        "ipython_config.py",
        # pipenv, UV, poetry, pdm, pixi
        ".venv",
        "env",
        "venv",
        "ENV",
        "env.bak",
        "venv.bak",
        ".pdm-python",
        ".pdm-build",
        ".pixi",
        # PEP 582
        "__pypackages__",
        # Celery
        "celerybeat-schedule",
        "celerybeat.pid",
        # Redis
        "*.rdb",
        "*.aof",
        "*.pid",
        # RabbitMQ
        "mnesia",
        "rabbitmq",
        "rabbitmq-data",
        # ActiveMQ
        "activemq-data",
        # SageMath
        "*.sage.py",
        # Environments
        #
        # Disabling env for now until environment variable feature is not implemented on platform
        # ".env",
        ".envrc",
        # IDE settings
        ".spyderproject",
        ".spyproject",
        ".ropeproject",
        # mkdocs
        "site",
        # Type checkers
        ".mypy_cache",
        ".dmypy.json",
        "dmypy.json",
        ".pyre",
        ".pytype",
        # Cython
        "cython_debug",
        # Abstra
        ".abstra",
        # Ruff
        ".ruff_cache",
        # PyPI
        ".pypirc",
        # Marimo
        "marimo/_static",
        "marimo/_lsp",
        "__marimo__",
        # Streamlit
        ".streamlit",
        # Git
        ".git",
        # CrewNode
        "node_modules",
    }

    def should_exclude(path: Path, relative_path: Path) -> bool:
        """Check if a path should be excluded based on patterns."""
        path_str = str(relative_path)
        path_parts = relative_path.parts

        for part in path_parts:
            for pattern in excluded_patterns:
                if part == pattern:
                    return True

                if fnmatch.fnmatch(part, pattern):
                    return True

        for pattern in excluded_patterns:
            if fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(
                path_str, f"*/{pattern}"
            ):
                return True

            if fnmatch.fnmatch(path.name, pattern):
                return True

        return False

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                relative_path = file_path.relative_to(directory)

                if should_exclude(file_path, relative_path):
                    continue

                console.print(f"[dim]Adding file: {relative_path}[/dim]")

                zip_file.write(file_path, relative_path)

    zip_buffer.seek(0)
    return zip_buffer
