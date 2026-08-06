"""Backward-compat import aliases for the 6.0 rename (atoms->agents, waves->speech).

Hand-maintained (see .fernignore). Attribute access (``smallestai.agents``) is
handled by the root ``__init__`` ``__getattr__``. This module installs a
``sys.meta_path`` finder so that *deep* imports of the old names keep working,
e.g. ``import smallestai.agents.crew.nodes`` or
``from smallestai.speech.helpers import synthesize_to_file``. Each such import
resolves to the new module and emits a ``DeprecationWarning`` once per old name.
Remove this shim in the next major.
"""

import importlib
import sys
import warnings
from importlib.abc import Loader, MetaPathFinder
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Optional, Sequence

# old top-level package -> new top-level package
_ALIASES = {
    "smallestai.atoms": "smallestai.agents",
    "smallestai.waves": "smallestai.speech",
}
_warned: set = set()


def _resolve(fullname: str) -> Optional[str]:
    for old, new in _ALIASES.items():
        if fullname == old or fullname.startswith(old + "."):
            return new + fullname[len(old):]
    return None


class _AliasLoader(Loader):
    def __init__(self, old_name: str, new_name: str) -> None:
        self._old_name = old_name
        self._new_name = new_name

    def create_module(self, spec: ModuleSpec) -> ModuleType:
        top = self._old_name.split(".", 2)[1]  # "atoms" or "waves"
        if top not in _warned:
            _warned.add(top)
            new_top = _ALIASES["smallestai." + top].split(".")[-1]
            warnings.warn(
                f"smallestai.{top} is deprecated and will be removed in a future "
                f"major version; use smallestai.{new_top} instead.",
                DeprecationWarning,
                stacklevel=2,
            )
        module = importlib.import_module(self._new_name)
        sys.modules[self._old_name] = module
        return module

    def exec_module(self, module: ModuleType) -> None:
        # The module already executed under its real name; nothing to do.
        pass


class _AliasFinder(MetaPathFinder):
    def find_spec(
        self, fullname: str, path: Optional[Sequence[str]] = None, target: Optional[ModuleType] = None
    ) -> Optional[ModuleSpec]:
        new_name = _resolve(fullname)
        if new_name is None:
            return None
        # No submodule_search_locations: the target may be a package, but we let
        # this finder handle every level (smallestai.atoms.crew.nodes -> ...) so
        # each aliased module is the *same object* as the real one, not a re-exec.
        return ModuleSpec(fullname, _AliasLoader(fullname, new_name))


def install_import_aliases() -> None:
    if not any(isinstance(f, _AliasFinder) for f in sys.meta_path):
        sys.meta_path.insert(0, _AliasFinder())


# --- Deprecated client attribute aliases (client.atoms -> client.agents, etc.) ---
# Applied lazily to the SmallestAI / AsyncSmallestAI classes when they are first
# imported (see the root __init__), so we don't eagerly import the client and
# defeat lazy loading.

_CLIENT_ALIASES = {"atoms": "agents", "waves": "speech"}


def _make_alias_property(old_name: str, new_name: str):
    def getter(self):
        warnings.warn(
            f"client.{old_name} is deprecated and will be removed in a future major "
            f"version; use client.{new_name} instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return getattr(self, new_name)

    return property(getter)


def add_deprecated_client_aliases(cls: type) -> None:
    if getattr(cls, "_smallestai_deprecated_aliases", False):
        return
    for old_name, new_name in _CLIENT_ALIASES.items():
        setattr(cls, old_name, _make_alias_property(old_name, new_name))
    setattr(cls, "_smallestai_deprecated_aliases", True)
