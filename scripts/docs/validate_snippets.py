#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs" / "v3"

FENCE_RE = re.compile(r"^```([a-zA-Z0-9_+-]*)\s*$")
SMART_QUOTES = ("“", "”", "‘", "’")
CHECK_LANGS = {"sql", "bash", "sh", "yaml", "json"}


def validate_file(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()

    in_fence = False
    fence_lang = ""
    fence_start = 0
    buf: list[str] = []

    for idx, line in enumerate(lines, start=1):
        match = FENCE_RE.match(line)
        if match:
            if not in_fence:
                in_fence = True
                fence_lang = match.group(1).lower()
                fence_start = idx
                buf = []
            else:
                if fence_lang in CHECK_LANGS:
                    content = "\n".join(buf).strip()
                    if not content:
                        errors.append(f"{path}:{fence_start} empty `{fence_lang}` code block")
                    for quote in SMART_QUOTES:
                        if quote in content:
                            errors.append(
                                f"{path}:{fence_start} smart quote found in `{fence_lang}` block"
                            )
                in_fence = False
                fence_lang = ""
                fence_start = 0
                buf = []
            continue

        if in_fence:
            buf.append(line)

    if in_fence:
        errors.append(f"{path}:{fence_start} unterminated code fence")
    return errors


def main() -> int:
    files = sorted(DOCS_ROOT.rglob("*.md"))
    all_errors: list[str] = []
    for file in files:
        all_errors.extend(validate_file(file))

    if all_errors:
        print("Snippet validation failed:")
        for err in all_errors[:200]:
            print(err)
        if len(all_errors) > 200:
            print(f"... truncated {len(all_errors) - 200} additional errors")
        return 1

    print(f"Snippet validation passed for {len(files)} markdown files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
