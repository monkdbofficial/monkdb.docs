#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs" / "v3"
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def is_external(target: str) -> bool:
    return (
        target.startswith("#")
        or target.startswith("mailto:")
        or target.startswith("http://")
        or target.startswith("https://")
        or target.startswith("tel:")
        or target.startswith("data:")
        or target.startswith("javascript:")
    )


def main() -> int:
    missing: list[str] = []
    for file in sorted(DOCS_ROOT.rglob("*.md")):
        text = file.read_text(encoding="utf-8", errors="ignore")
        for match in LINK_RE.finditer(text):
            target = match.group(1).strip().strip("<>").split(" ")[0]
            if is_external(target):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if not target or target.endswith(".pdf"):
                continue
            if target.startswith("/"):
                resolved = REPO_ROOT / target.lstrip("/")
            else:
                resolved = (file.parent / target).resolve()
            if not resolved.exists():
                missing.append(f"{file}:{target}")

    if missing:
        print("Broken relative links:")
        for item in missing[:200]:
            print(item)
        if len(missing) > 200:
            print(f"... truncated {len(missing) - 200} more")
        return 1

    print("All markdown links resolved (excluding external and PDF links).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
