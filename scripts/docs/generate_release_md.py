#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re


REPO_ROOT = pathlib.Path(__file__).resolve().parents[2]
RELEASE_SRC = REPO_ROOT / "v3" / "releases"
RELEASE_DST = REPO_ROOT / "v3" / "release.md"


def version_key(version: str) -> tuple[int, int, int]:
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)$", version)
    if not m:
        return (0, 0, 0)
    return tuple(int(g) for g in m.groups())  # type: ignore[return-value]


def main() -> int:
    files = sorted(RELEASE_SRC.glob("*.md"),
                   key=lambda p: version_key(p.stem), reverse=True)
    lines: list[str] = ["# Release Notes", "",
                        "This page tracks feature highlights by MonkDB release.", ""]

    for file in files:
        version = file.stem
        body = file.read_text(encoding="utf-8", errors="ignore").strip()
        body = body.replace("(../features/", "(./features/")
        lines.append(f"## {version}")
        lines.append("")
        lines.extend(body.splitlines())
        lines.append("")

    RELEASE_DST.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(
        f"Generated {RELEASE_DST.relative_to(REPO_ROOT)} from {len(files)} release fragments.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
