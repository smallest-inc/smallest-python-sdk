# Hand-maintained (see .fernignore). Based on the generated root __init__, plus:
#  - custom exports (PlanNotEntitledError, the `errors` module),
#  - deprecated 6.0 back-compat aliases for the old `atoms` / `waves` names.
# Re-apply these after a regen.

# isort: skip_file

import typing
import warnings
from importlib import import_module

if typing.TYPE_CHECKING:
    from . import agents, errors, speech
    from ._default_clients import DefaultAioHttpClient, DefaultAsyncHttpxClient
    from .agents.client import AgentsClient, AsyncAgentsClient
    from .agents.errors.bad_request_error import PlanNotEntitledError
    from .client import AsyncSmallestAI, SmallestAI
    from .environment import SmallestAIEnvironment
    from .speech.client import AsyncSpeechClient, SpeechClient
    from .version import __version__

_dynamic_imports: typing.Dict[str, str] = {
    "AgentsClient": ".agents.client",
    "AsyncAgentsClient": ".agents.client",
    "AsyncSmallestAI": ".client",
    "AsyncSpeechClient": ".speech.client",
    "DefaultAioHttpClient": "._default_clients",
    "DefaultAsyncHttpxClient": "._default_clients",
    "PlanNotEntitledError": ".agents.errors.bad_request_error",
    "SmallestAI": ".client",
    "SmallestAIEnvironment": ".environment",
    "SpeechClient": ".speech.client",
    "__version__": ".version",
    "agents": ".agents",
    "errors": ".errors",
    "speech": ".speech",
}

# Deprecated 6.0 aliases: old product names -> new. Attribute access
# (smallestai.atoms) is handled here; deep imports (import smallestai.atoms.crew)
# are handled by the import hook installed at the bottom of this file.
_DEPRECATED_ALIASES = {"atoms": "agents", "waves": "speech"}


def __getattr__(attr_name: str) -> typing.Any:
    if attr_name in _DEPRECATED_ALIASES:
        new = _DEPRECATED_ALIASES[attr_name]
        warnings.warn(
            f"smallestai.{attr_name} is deprecated and will be removed in a future "
            f"major version; use smallestai.{new} instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return import_module(f".{new}", __package__)

    module_name = _dynamic_imports.get(attr_name)
    if module_name is None:
        raise AttributeError(f"No {attr_name} found in _dynamic_imports for module name -> {__name__}")
    try:
        module = import_module(module_name, __package__)
        if module_name == f".{attr_name}":
            return module
        obj = getattr(module, attr_name)
        if attr_name in ("SmallestAI", "AsyncSmallestAI"):
            from ._compat import add_deprecated_client_aliases
            add_deprecated_client_aliases(obj)
        return obj
    except ImportError as e:
        raise ImportError(f"Failed to import {attr_name} from {module_name}: {e}") from e
    except AttributeError as e:
        raise AttributeError(f"Failed to get {attr_name} from {module_name}: {e}") from e


def __dir__():
    return sorted(list(_dynamic_imports.keys()) + list(_DEPRECATED_ALIASES.keys()))


__all__ = [
    "AgentsClient",
    "AsyncAgentsClient",
    "AsyncSmallestAI",
    "AsyncSpeechClient",
    "DefaultAioHttpClient",
    "DefaultAsyncHttpxClient",
    "PlanNotEntitledError",
    "SmallestAI",
    "SmallestAIEnvironment",
    "SpeechClient",
    "__version__",
    "agents",
    "errors",
    "speech",
]

# Keep `import smallestai.atoms.crew...` (and .waves...) working, deprecated.
from ._compat import install_import_aliases as _install_import_aliases

_install_import_aliases()
