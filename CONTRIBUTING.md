# Contributing to Subscan

Thanks for helping improve Subscan. Contributions that improve reliability, portability, testing, documentation, or safe authorized-use workflows are welcome.

## Before you start

- Use Subscan only on systems you own or have explicit permission to test.
- Search existing issues and pull requests before starting duplicate work.
- Keep pull requests focused on one logical change.
- Do not include credentials, private targets, vulnerability details under coordinated disclosure, or data collected from third parties.

## Development setup

```bash
git clone https://github.com/bhatmuneeb1/subscan.git
cd subscan
python -m venv .venv
source .venv/bin/activate
python -m pip install -e . pytest
pytest
```

## Pull requests

A strong pull request should include:

1. A clear explanation of the problem.
2. The smallest reasonable implementation.
3. Tests for behavior changes when practical.
4. Documentation updates for user-facing changes.
5. Confirmation that `pytest` passes.

Please avoid changes whose sole purpose is contribution-count inflation, generated noise, or unrelated formatting churn.

## Good first contributions

- Add platform-specific setup documentation.
- Improve tool-presence diagnostics.
- Add tests for input parsing and output normalization.
- Improve error handling for third-party tools.
- Add structured JSON output.
- Improve documentation for authorized testing workflows.

## Security issues

Do not open public issues for vulnerabilities in Subscan itself. Follow `SECURITY.md` instead.
