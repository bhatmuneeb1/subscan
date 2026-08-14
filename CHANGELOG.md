# Changelog

All notable project changes are documented here.

## [0.2.0] - 2026-08-14

### Added
- Command-line arguments and `--check-tools` diagnostics.
- Domain validation and normalization.
- Modern Python packaging through `pyproject.toml`.
- Unit tests and GitHub Actions CI across Python 3.10-3.12.
- MIT license, contributor guide, and security policy.

### Changed
- Replaced shell-based command construction with `subprocess` argument lists.
- Made third-party tool execution tolerant of missing optional tools.
- Normalized and deduplicated generated output in Python.

### Security
- Removed direct interpolation of user-controlled domain input into shell commands.

## [0.1.0]
- Initial public reconnaissance orchestration script.
