#!/usr/bin/env python3
"""Switch generated HTML between compact and readable formatting."""

from argparse import ArgumentParser
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).parent
DIST = ROOT / "docs"


def compact(document):
    return re.sub(r"\s+", " ", document).strip() + "\n"


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("compact", "tidy"))
    args = parser.parse_args()

    pages = sorted(DIST.rglob("*.html"))
    if not pages:
        parser.error("no generated HTML files found; run make build first")

    if args.mode == "compact":
        for page in pages:
            page.write_text(compact(page.read_text(encoding="utf-8")), encoding="utf-8")
    else:
        subprocess.run(
            ["prettier", "--write", *(str(page) for page in pages)],
            check=True,
        )

    print(f"Formatted {len(pages)} HTML files as {args.mode}.")


if __name__ == "__main__":
    main()
