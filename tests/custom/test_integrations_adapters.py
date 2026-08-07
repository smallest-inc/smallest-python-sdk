"""smallestai.integrations.* lazy framework adapters.

Importing an adapter module must never require the framework. Accessing a name
either forwards to the framework plugin (if installed) or raises a clear
"install the extra" ImportError.
"""

import importlib

import pytest


def _framework_installed(module_path: str) -> bool:
    try:
        importlib.import_module(module_path)
        return True
    except ImportError:
        return False


def test_importing_adapter_modules_never_requires_framework():
    # Must import cleanly whether or not pipecat/livekit are present.
    importlib.import_module("smallestai.integrations.pipecat")
    importlib.import_module("smallestai.integrations.livekit")


def test_pipecat_adapter_forwards_or_raises_clear_error():
    import smallestai.integrations.pipecat as pc

    if _framework_installed("pipecat.services.smallest"):
        import pipecat.services.smallest as real  # type: ignore[import-not-found]

        assert pc.SmallestSTTService is real.SmallestSTTService
        assert "SmallestSTTService" in dir(pc)
    else:
        with pytest.raises(ImportError) as ei:
            _ = pc.SmallestSTTService
        assert "smallestai[pipecat]" in str(ei.value)
        assert dir(pc) == []


def test_livekit_adapter_forwards_or_raises_clear_error():
    import smallestai.integrations.livekit as lk

    if _framework_installed("livekit.plugins.smallestai"):
        import livekit.plugins.smallestai as real  # type: ignore[import-not-found]

        assert lk.TTS is real.TTS
    else:
        with pytest.raises(ImportError) as ei:
            _ = lk.TTS
        assert "smallestai[livekit]" in str(ei.value)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
