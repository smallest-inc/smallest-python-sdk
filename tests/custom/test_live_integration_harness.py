"""Offline regressions for the live harness; never call the live tests."""

import importlib.util
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from zipfile import ZipFile

import httpx
import pytest

ROOT = Path(__file__).resolve().parents[2]


def load_harness(name, monkeypatch):
    monkeypatch.setenv("SMALLEST_API_KEY", "test-key")
    spec = importlib.util.spec_from_file_location(name, ROOT / "tests/integration" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("name", ["test_caller_context_live", "test_sdk_smoke_live"])
@pytest.mark.parametrize(
    "base", ["http://127.0.0.1:9999", "https://api.india.smallest.ai", "https://api.dev.smallest.ai"]
)
def test_sdk_targets_selected_host(name, base, monkeypatch):
    monkeypatch.setenv("SMALLEST_BASE", base)
    module = load_harness(name, monkeypatch)
    seen = []
    real_client = httpx.Client

    def respond(request):
        seen.append(request)
        return httpx.Response(200, json={"status": "success", "data": []})

    monkeypatch.setattr(httpx, "Client", lambda **kwargs: real_client(**kwargs, transport=httpx.MockTransport(respond)))
    module._client().atoms.phone_numbers.list()
    assert len(seen) == 1
    assert str(seen[0].url).startswith(base + "/atoms/v1/")
    assert seen[0].headers["Authorization"] == "Bearer test-key"


def test_probe_bundle_installs_checkout_wheel(tmp_path, monkeypatch):
    module = load_harness("test_caller_context_live", monkeypatch)
    wheel_name = "smallestai-5.14.0-py3-none-any.whl"

    def build(args, **kwargs):
        assert args[:7] == [sys.executable, "-m", "pip", "wheel", "--no-deps", "--no-build-isolation", "--wheel-dir"]
        assert args[-1] == str(ROOT)
        (tmp_path / wheel_name).write_bytes(b"wheel built from this checkout")
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr(module.subprocess, "run", build)
    module._build_probe_package(tmp_path)
    from smallestai.cli.utils import create_zip_from_directory

    with ZipFile(create_zip_from_directory(tmp_path)) as bundle:
        import tomli

        project = tomli.loads(bundle.read("pyproject.toml").decode())
        assert project["tool"]["poetry"]["dependencies"]["smallestai"] == {"path": wheel_name}
        assert "requirements.txt" not in bundle.namelist()
        assert bundle.read(wheel_name) == b"wheel built from this checkout"
        assert bundle.read("server.py").decode() == module.PROBE_SERVER


@pytest.mark.parametrize("stage", ["success", "init", "deploy"])
def test_deploy_uses_same_host_and_no_login(stage, monkeypatch):
    module = load_harness("test_caller_context_live", monkeypatch)
    module.BASE = "https://api.india.smallest.ai"
    monkeypatch.setenv("SMALLEST_BASE_URL", "https://unrelated.example")
    monkeypatch.setattr(module, "_build_probe_package", lambda path: None)
    seen = []

    def run(args, **kwargs):
        seen.append((args, kwargs))
        assert args[:2] == [sys.executable, str(ROOT / "tests/integration/_crew_cli.py")]
        assert kwargs["env"]["SMALLEST_BASE_URL"] == module.BASE
        assert kwargs["env"]["SMALLEST_API_KEY"] == "test-key"
        assert kwargs["env"]["PYTHONPATH"] == str(ROOT / "src")
        assert "test-key" not in " ".join(args)
        assert "auth" not in args
        return SimpleNamespace(returncode=int(args[2] == stage), stdout="Build ID: build-1\nSUCCEEDED", stderr="failed")

    monkeypatch.setattr(module.subprocess, "run", run)
    if stage == "success":
        assert module._deploy_probe_crew("agent-1") == "build-1"
    else:
        with pytest.raises(AssertionError, match=f"{stage} failed"):
            module._deploy_probe_crew("agent-1")
    assert not Path(seen[0][1]["cwd"]).exists()


def test_crew_runner_uses_real_cli_without_auth_files(tmp_path):
    env = {
        **os.environ,
        "SMALLEST_API_KEY": "test-key",
        "SMALLEST_BASE_URL": "https://api.example",
        "PYTHONPATH": str(ROOT / "src"),
    }
    result = subprocess.run(
        [sys.executable, str(ROOT / "tests/integration/_crew_cli.py"), "init", "--agent-id", "agent-1"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
    assert "agent-1" in (tmp_path / ".smallestai/config.toml").read_text()
    assert not (tmp_path / ".smallestai/credentials.json").exists()


def test_make_live_uses_selected_host(monkeypatch):
    module = load_harness("test_caller_context_live", monkeypatch)
    module.BASE = "http://127.0.0.1:9999"
    from unittest.mock import MagicMock

    response = MagicMock()
    response.__enter__.return_value.status = 200

    def urlopen(request, timeout):
        assert request.full_url == module.BASE + "/atoms/v1/sdk/agents/agent/builds/build"
        assert request.method == "PATCH"
        assert request.get_header("Authorization") == "Bearer test-key"
        assert request.data == b'{"isLive": true}'
        return response

    monkeypatch.setattr(module.urllib.request, "urlopen", urlopen)
    module._set_build_live("agent", "build")


def test_wheel_failure_stops_deployment_and_cleans_up(monkeypatch):
    module = load_harness("test_caller_context_live", monkeypatch)
    seen = []

    def fail(args, **kwargs):
        seen.append(args)
        raise subprocess.CalledProcessError(1, args)

    monkeypatch.setattr(module.subprocess, "run", fail)
    with pytest.raises(subprocess.CalledProcessError):
        module._deploy_probe_crew("agent")
    assert len(seen) == 1
    assert seen[0][2:4] == ["pip", "wheel"]
    assert not Path(seen[0][7]).exists()
