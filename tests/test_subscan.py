from pathlib import Path

import pytest

import subscan


@pytest.mark.parametrize(
    "value,expected",
    [
        ("example.com", "example.com"),
        ("EXAMPLE.COM.", "example.com"),
        ("sub.example.co.uk", "sub.example.co.uk"),
    ],
)
def test_normalize_domain_accepts_valid_domains(value, expected):
    assert subscan.normalize_domain(value) == expected


@pytest.mark.parametrize(
    "value",
    [
        "https://example.com",
        "example.com;id",
        "example.com && whoami",
        "127.0.0.1",
        "localhost",
        "",
    ],
)
def test_normalize_domain_rejects_unsafe_or_invalid_input(value):
    with pytest.raises(ValueError):
        subscan.normalize_domain(value)


def test_write_sorted_deduplicates(tmp_path: Path):
    target = tmp_path / "out.txt"
    subscan.write_sorted(target, ["b.example.com", "a.example.com", "b.example.com"])
    assert target.read_text() == "a.example.com\nb.example.com\n"


def test_check_tools_mode_returns_success(monkeypatch, capsys):
    monkeypatch.setattr(subscan, "available_tools", lambda: {"subfinder": True, "httpx": False})
    assert subscan.main(["--check-tools"]) == 0
    output = capsys.readouterr().out
    assert "OK" in output
    assert "MISSING" in output
