"""Banner rendering: ring rasterisation, static/compact/animated paths."""

import smallestai.cli.banner as banner


def test_rings_shape_and_width():
    lines = banner._rings(banner._BASE_RADII)
    assert len(lines) == banner._RING_ROWS
    assert all(len(line) == banner._RING_COLS for line in lines)


def test_static_banner_has_wordmark(capsys, monkeypatch):
    # Wide, non-animated: single static frame, full wordmark.
    monkeypatch.setattr(banner, "_term_width", lambda: 120)
    monkeypatch.setattr(banner, "_animate_enabled", lambda: False)
    banner.print_banner()
    out = capsys.readouterr().out
    assert banner._WORDMARK[0] in out


def test_compact_fallback_on_narrow(capsys, monkeypatch):
    monkeypatch.setattr(banner, "_term_width", lambda: 60)
    banner.print_banner()
    out = capsys.readouterr().out
    assert "SMALLEST AI" in out
    assert banner._WORDMARK[0] not in out  # no big figlet when narrow


def test_animated_path_runs(capsys, monkeypatch):
    # Force the animated branch but no real sleeping.
    monkeypatch.setattr(banner, "_term_width", lambda: 120)
    monkeypatch.setattr(banner, "_animate_enabled", lambda: True)
    monkeypatch.setattr(banner, "_color_enabled", lambda: True)
    monkeypatch.setattr(banner.time, "sleep", lambda _s: None)
    banner.print_banner()
    out = capsys.readouterr().out
    assert banner._WORDMARK[0] in out
    assert "\033[?25l" in out and "\033[?25h" in out  # cursor hidden then restored


if __name__ == "__main__":
    import pytest

    pytest.main([__file__, "-v"])
