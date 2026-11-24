#!/usr/bin/env python3
"""Build an importable WorkBuddy / CodeBuddy expert zip from this repository.

Usage:
    python scripts/build-package.py            # write dist/virtual-drone-expert.zip
    python scripts/build-package.py --check    # validate only, write nothing

Standard library only. Run from anywhere; paths are resolved relative to the
repository root (the parent of this script's directory).
"""

from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE_NAME = "virtual-drone-expert"
PLUGIN_JSON = Path(".codebuddy-plugin/plugin.json")
REQUIRED_PLUGIN_FIELDS = ("name", "version", "expertType", "agentName", "agents")

# Files that go into the importable zip, relative to the repository root.
PACKAGE_FILES = (
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    ".codebuddy-plugin/plugin.json",
    "agents/virtual-drone-expert.md",
    "avatars/expert.png",
)


def validate() -> list[str]:
    """Return a list of problems; empty means the package is valid."""
    problems: list[str] = []

    plugin_path = ROOT / PLUGIN_JSON
    if not plugin_path.is_file():
        return [f"missing {PLUGIN_JSON}"]

    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"invalid {PLUGIN_JSON}: {exc}"]

    for field in REQUIRED_PLUGIN_FIELDS:
        if field not in plugin:
            problems.append(f"plugin.json missing required field: {field}")

    if plugin.get("name") != PACKAGE_NAME:
        problems.append(f"plugin.json name should be {PACKAGE_NAME!r}, got {plugin.get('name')!r}")
    if plugin.get("agentName") != PACKAGE_NAME:
        problems.append("plugin.json agentName does not match package name")

    for agent_rel in plugin.get("agents", []):
        if not (ROOT / agent_rel).is_file():
            problems.append(f"agent file not found: {agent_rel}")

    avatar = ROOT / "avatars" / "expert.png"
    if not avatar.is_file():
        problems.append("missing avatars/expert.png")
    elif avatar.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
        problems.append("avatars/expert.png is not a valid PNG")

    for rel in PACKAGE_FILES:
        if not (ROOT / rel).is_file():
            problems.append(f"package file missing: {rel}")

    return problems


def build() -> Path:
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / f"{PACKAGE_NAME}.zip"

    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for rel in PACKAGE_FILES:
            zf.write(ROOT / rel, f"{PACKAGE_NAME}/{rel}")

    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="validate only, do not write the zip")
    args = parser.parse_args()

    problems = validate()
    if problems:
        for p in problems:
            print(f"[FAIL] {p}", file=sys.stderr)
        return 1
    print("[OK] package structure is valid")

    if args.check:
        return 0

    out = build()
    print(f"[OK] wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
