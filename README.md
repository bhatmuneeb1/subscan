# Subscan

A small, open-source orchestration CLI for **authorized subdomain reconnaissance**. Subscan coordinates established third-party tools, normalizes their output, and helps security researchers avoid repetitive manual glue work.

> Use Subscan only against systems you own or have explicit permission to test.

## Why Subscan?

Reconnaissance often means running several tools, collecting overlapping output, checking which hosts are live, and then passing those results into follow-up checks. Subscan turns that workflow into one repeatable command while keeping the underlying tools visible and replaceable.

## Features

- Validates and normalizes target domain names before execution.
- Invokes external tools without a shell to reduce command-injection risk.
- Supports Sublist3r, Assetfinder, Findomain, Subfinder, and Amass.
- Probes discovered hosts with httpx and httprobe when installed.
- Can run Subjack and Subzy checks against live results.
- Deduplicates output into simple text files.
- Detects missing tools and continues with what is available.
- Includes unit tests and CI for Python 3.10, 3.11, and 3.12.

## Installation

### From source

```bash
git clone https://github.com/bhatmuneeb1/subscan.git
cd subscan
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

The Python package itself has no runtime dependency on the third-party reconnaissance tools. Install whichever external tools you want Subscan to orchestrate.

Check what is available:

```bash
subscan --check-tools
```

## Usage

Run a scan against an authorized domain:

```bash
subscan example.com
```

Choose an output directory:

```bash
subscan example.com --output results/example
```

Skip takeover checks:

```bash
subscan example.com --skip-takeover
```

You can also run the module directly:

```bash
python subscan.py example.com
```

## Output

A typical run can create files such as:

```text
example.com_output/
├── sublist3r.txt
├── assetfinder.txt
├── findomain.txt
├── subfinder.txt
├── amass.txt
├── subdomains.txt
├── alive_httpx.txt
├── alive_httprobe.txt
├── alive_subdomains.txt
└── subjack_results.txt
```

Exact files depend on which third-party tools are installed and return results.

## Development

```bash
python -m pip install -e . pytest
pytest
```

GitHub Actions runs the test suite on supported Python versions for pushes and pull requests.

## Contributing

Contributions are welcome, especially improvements to reliability, portability, testing, structured output, documentation, and safe authorized-use workflows. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

If you find a vulnerability in Subscan itself, please follow [SECURITY.md](SECURITY.md) rather than opening a public issue with exploit details.

## Project status

Subscan is being modernized from its original proof-of-concept script into a maintainable CLI. The current `0.2.x` line focuses on safer process execution, reproducibility, testing, and contributor experience.

See [CHANGELOG.md](CHANGELOG.md) for notable changes.

## License

MIT — see [LICENSE](LICENSE).

## Responsible use

Subscan is intended for security research, defensive assessment, education, and bug-bounty work where the operator has authorization. You are responsible for following applicable laws and each target's testing rules.
