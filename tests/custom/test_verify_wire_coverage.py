"""Regression tests for namespace matching in the static wire coverage gate."""

import importlib.util
from pathlib import Path

import pytest


@pytest.mark.parametrize("waves_first", [True, False])
def test_wire_coverage_matches_atoms_namespace(tmp_path, monkeypatch, capsys, waves_first):
    spec = importlib.util.spec_from_file_location(
        "verify", Path(__file__).resolve().parents[2] / "scripts" / "verify.py"
    )
    verify = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verify)

    analytics = tmp_path / "src" / "atoms" / "analytics"
    analytics.mkdir(parents=True)
    (analytics / "client.py").write_text("class Client:\n    def get_summary(self): pass\n")
    wire = tmp_path / "wire"
    wire.mkdir()
    atoms = wire / "test_atoms_analytics.py"
    waves = wire / "test_waves_analytics.py"
    atoms.write_text("def test_atoms_analytics_get_summary(): pass\n")
    waves.write_text("")
    monkeypatch.setattr(verify, "SRC", tmp_path / "src")
    monkeypatch.setattr(verify, "WIRE", wire)
    original_glob = Path.glob

    def ordered_glob(path, pattern):
        if path == wire:
            return iter([waves, atoms] if waves_first else [atoms, waves])
        return original_glob(path, pattern)

    monkeypatch.setattr(Path, "glob", ordered_glob)
    verify.check_wire_coverage()
    assert verify.failures == []
    assert "methods=1 wiretests=1" in capsys.readouterr().out

    # Waves tests cannot satisfy missing Atoms coverage, regardless of order.
    atoms.write_text("")
    waves.write_text("def test_waves_analytics_get_summary(): pass\n")
    verify.check_wire_coverage()
    assert verify.failures == ["wire: analytics has 0 wire tests for 1 methods"]
