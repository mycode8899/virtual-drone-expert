# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [Semantic Versioning](https://semver.org/).

## [1.0.0] - 2026-11-24

First public release of the expert package, with a complete open-source documentation set.

### Added

- Core Agent prompt: `agents/virtual-drone-expert.md`
  - Explicit input contract, five camera-path presets, a camera parameter table, output specification and a graceful-degradation branch.
- Expert metadata: `.codebuddy-plugin/plugin.json` (bilingual display name, description, quick prompts).
- Avatar: `avatars/expert.png`.
- Documentation: Chinese and English READMEs, `docs/principles.md`, `docs/installation.md`, `docs/prompt-examples.md`, `docs/faq.md`.
- Project files: `LICENSE` (MIT), `CONTRIBUTING.md`, `.gitignore`, GitHub issue / PR templates.
- `scripts/build-package.py` to rebuild the importable zip from source.

### Fixed

- Unified the typo `GAT6` to `GTA6` across the prompt, metadata and documentation.
- Removed an unverifiable personal attribution for the Reality View technical breakdown; replaced with links to public reporting and an explicit note that reported figures are vendor / press claims.
- Clarified that the package is a prompt-based expert and does **not** ship model weights, inference code, or third-party API calls.
- Added trademark, source-material copyright, and "no factual use" disclaimers.

### Notes

- The original four-file archive (`README.md`, `.codebuddy-plugin/plugin.json`, `agents/`, `avatars/`) remains functionally unchanged apart from the fixes above; importing behaviour is preserved.

[1.0.0]: https://github.com/mycode8899/virtual-drone-expert/releases/tag/v1.0.0
