#!/usr/bin/env python3
"""Subscan: orchestrate passive subdomain reconnaissance tools safely.

Subscan does not implement scanners itself. It validates the target, invokes
installed third-party tools without a shell, and normalizes their output.
Only run it against systems you own or are explicitly authorized to test.
"""

from __future__ import annotations

import argparse
import ipaddress
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

DOMAIN_RE = re.compile(
    r"^(?=.{1,253}\.?$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[A-Za-z]{2,63}\.?$"
)

ENUMERATORS = {
    "sublist3r": lambda domain, out: ["sublist3r", "-d", domain, "-o", str(out)],
    "assetfinder": lambda domain, out: ["assetfinder", "--subs-only", domain],
    "findomain": lambda domain, out: ["findomain", "-t", domain, "-u", str(out)],
    "subfinder": lambda domain, out: ["subfinder", "-d", domain, "-o", str(out)],
    "amass": lambda domain, out: ["amass", "enum", "-passive", "-d", domain, "-o", str(out)],
}


def normalize_domain(value: str) -> str:
    """Validate and normalize a DNS domain name."""
    domain = value.strip().rstrip(".").lower()
    if not domain or "/" in domain or "://" in domain:
        raise ValueError("enter a domain name such as example.com, not a URL")
    try:
        ipaddress.ip_address(domain)
    except ValueError:
        pass
    else:
        raise ValueError("IP addresses are not accepted; provide a DNS domain")
    if not DOMAIN_RE.fullmatch(domain):
        raise ValueError(f"invalid domain name: {value!r}")
    return domain


def available_tools() -> dict[str, bool]:
    names = [*ENUMERATORS, "httprobe", "httpx", "subjack", "subzy"]
    return {name: shutil.which(name) is not None for name in names}


def run(command: Sequence[str], *, stdout_file: Path | None = None) -> int:
    """Run a command without invoking a shell."""
    print("[+]", " ".join(command))
    try:
        if stdout_file:
            with stdout_file.open("w", encoding="utf-8") as handle:
                completed = subprocess.run(command, stdout=handle, stderr=subprocess.PIPE, text=True, check=False)
        else:
            completed = subprocess.run(command, check=False)
    except OSError as exc:
        print(f"[!] failed to execute {command[0]}: {exc}", file=sys.stderr)
        return 127

    if completed.returncode != 0:
        print(f"[!] {command[0]} exited with status {completed.returncode}", file=sys.stderr)
        stderr = getattr(completed, "stderr", "")
        if stderr:
            print(stderr.strip(), file=sys.stderr)
    return completed.returncode


def read_lines(paths: Iterable[Path]) -> set[str]:
    values: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            item = line.strip()
            if item:
                values.add(item)
    return values


def write_sorted(path: Path, values: Iterable[str]) -> None:
    path.write_text("".join(f"{value}\n" for value in sorted(set(values))), encoding="utf-8")


def enumerate_subdomains(domain: str, output: Path, tools: dict[str, bool]) -> Path:
    generated: list[Path] = []
    for tool, command_builder in ENUMERATORS.items():
        if not tools.get(tool):
            print(f"[-] skipping {tool}: not installed")
            continue
        destination = output / f"{tool}.txt"
        command = command_builder(domain, destination)
        if tool == "assetfinder":
            run(command, stdout_file=destination)
        else:
            run(command)
        generated.append(destination)

    combined = output / "subdomains.txt"
    write_sorted(combined, read_lines(generated))
    return combined


def probe_alive(subdomains: Path, output: Path, tools: dict[str, bool]) -> Path:
    generated: list[Path] = []
    if tools.get("httpx"):
        path = output / "alive_httpx.txt"
        run(["httpx", "-l", str(subdomains), "-o", str(path)])
        generated.append(path)

    if tools.get("httprobe"):
        path = output / "alive_httprobe.txt"
        with subdomains.open("r", encoding="utf-8") as source, path.open("w", encoding="utf-8") as destination:
            print("[+] httprobe")
            subprocess.run(["httprobe"], stdin=source, stdout=destination, check=False)
        generated.append(path)

    alive = output / "alive_subdomains.txt"
    write_sorted(alive, read_lines(generated))
    return alive


def takeover_checks(alive: Path, output: Path, tools: dict[str, bool]) -> None:
    if not alive.exists() or alive.stat().st_size == 0:
        print("[-] no live targets available for takeover checks")
        return
    if tools.get("subjack"):
        run(["subjack", "-w", str(alive), "-t", "50", "-timeout", "15", "-v", "-o", str(output / "subjack_results.txt")])
    if tools.get("subzy"):
        run(["subzy", "run", "--targets", str(alive)])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Authorized subdomain reconnaissance orchestrator")
    parser.add_argument("domain", nargs="?", help="authorized target domain, e.g. example.com")
    parser.add_argument("-o", "--output", type=Path, help="output directory")
    parser.add_argument("--skip-takeover", action="store_true", help="skip takeover checks")
    parser.add_argument("--check-tools", action="store_true", help="show installed external tools and exit")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    tools = available_tools()

    if args.check_tools:
        for name, present in tools.items():
            print(f"{'OK' if present else 'MISSING':7} {name}")
        return 0

    if not args.domain:
        print("error: domain is required unless --check-tools is used", file=sys.stderr)
        return 2

    try:
        domain = normalize_domain(args.domain)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    output = args.output or Path(f"{domain}_output")
    output.mkdir(parents=True, exist_ok=True)

    subdomains = enumerate_subdomains(domain, output, tools)
    alive = probe_alive(subdomains, output, tools)
    if not args.skip_takeover:
        takeover_checks(alive, output, tools)

    print(f"[+] results written to {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
