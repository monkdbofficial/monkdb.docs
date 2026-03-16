#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs" / "v3"

COMMAND_REQUIRED = [
    "## Command Snapshot",
    "## Purpose",
    "## Syntax",
    "## Operational Notes",
    "## When to Use",
    "## When Not to Use",
    "## Common Errors and Troubleshooting",
    "## Cross-References",
]

FUNCTION_REQUIRED = [
    "## Function Snapshot",
    "## Purpose",
    "## Syntax",
    "## Parameters",
    "## Returns",
    "## Null and Error Behavior",
    "## Operational Notes",
    "## Cross-References",
]


def audit(files: list[pathlib.Path], required: list[str]) -> list[tuple[pathlib.Path, list[str]]]:
    failures: list[tuple[pathlib.Path, list[str]]] = []
    for file in files:
        text = file.read_text(encoding="utf-8", errors="ignore")
        missing = [h for h in required if h not in text]
        if missing:
            failures.append((file, missing))
    return failures


def main() -> int:
    command_files = sorted((DOCS_ROOT / "sql" / "commands").glob("*.md"))
    command_files = [p for p in command_files if p.name != "README.md"]
    function_files = sorted((DOCS_ROOT / "sql" / "scalar-functions" / "functions").glob("*.md"))

    command_failures = audit(command_files, COMMAND_REQUIRED)
    function_failures = audit(function_files, FUNCTION_REQUIRED)

    print(f"Commands audited: {len(command_files)}")
    print(f"Functions audited: {len(function_files)}")
    print(f"Command failures: {len(command_failures)}")
    print(f"Function failures: {len(function_failures)}")

    for file, missing in command_failures[:50]:
        rel = file.relative_to(REPO_ROOT)
        print(f"[COMMAND] {rel} missing: {', '.join(missing)}")
    for file, missing in function_failures[:50]:
        rel = file.relative_to(REPO_ROOT)
        print(f"[FUNCTION] {rel} missing: {', '.join(missing)}")

    return 1 if command_failures or function_failures else 0


if __name__ == "__main__":
    sys.exit(main())
