"""Charge les modules depuis __pycache__ lorsque les sources sont absentes ou vides.

Le dépôt ne contient pas le code source complet ; les .pyc (Python 3.11) sont utilisés.
Ce hook doit être importé avant tout autre import local (voir main.py).
"""

from __future__ import annotations

import importlib.abc
import importlib.machinery
import importlib.util
import sys
from pathlib import Path

# Répertoire racine du jeu (sources ou extrait PyInstaller)
ROOT = Path(__file__).resolve().parent

# Modules / paquets racine gérés par le bytecode du projet
_TOP = frozenset(
    {
        "config",
        "utils",
        "sprite_registry",
        "entities",
        "game",
        "objects",
        "rooms",
        "systems",
        "ui",
    }
)

_TAG = "cpython-311"


class _PycLoader(importlib.machinery.SourcelessFileLoader):
    """Garantit que `__file__` est présent dans le `__dict__` du module (requis par le bytecode)."""

    def exec_module(self, module: object) -> None:
        module.__dict__["__file__"] = self.path
        super().exec_module(module)


def _source_override_path(fullname: str) -> Path | None:
    """Chemin du .py s'il existe et n'est pas vide (priorité sur le bytecode)."""
    parts = fullname.split(".")
    if len(parts) == 1:
        py = ROOT / f"{parts[0]}.py"
    else:
        py = ROOT / parts[0] / f"{parts[-1]}.py"
    if py.is_file() and py.stat().st_size > 0:
        return py
    return None


def _pyc_path_for(fullname: str) -> Path | None:
    parts = fullname.split(".")
    if not parts or parts[0] not in _TOP:
        return None

    if _source_override_path(fullname) is not None:
        return None

    if len(parts) == 1:
        name = parts[0]
        pkg_init = ROOT / name / "__pycache__" / f"__init__.{_TAG}.pyc"
        root_mod = ROOT / "__pycache__" / f"{name}.{_TAG}.pyc"
        if pkg_init.is_file():
            return pkg_init
        if root_mod.is_file():
            return root_mod
        return None

    sub = parts[-1]
    pkg = parts[0]
    return ROOT / pkg / "__pycache__" / f"{sub}.{_TAG}.pyc"


class _PycFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname: str, path: object, target: object | None = None):
        pyc = _pyc_path_for(fullname)
        if pyc is None or not pyc.is_file():
            return None
        loader = _PycLoader(fullname, str(pyc))
        parts = fullname.split(".")
        if len(parts) == 1 and pyc.name.startswith("__init__."):
            pkg_root = str(ROOT / parts[0])
            spec = importlib.util.spec_from_loader(
                fullname,
                loader,
                origin=str(pyc),
                is_package=True,
            )
            spec.submodule_search_locations = [pkg_root]
            return spec
        return importlib.util.spec_from_loader(fullname, loader, origin=str(pyc))


def install() -> None:
    global ROOT
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        ROOT = Path(sys._MEIPASS)
    finder = _PycFinder()
    if finder not in sys.meta_path:
        sys.meta_path.insert(0, finder)
