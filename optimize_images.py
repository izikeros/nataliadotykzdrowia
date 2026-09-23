#!/usr/bin/env python3
"""Generate WebP and AVIF copies of generated raster images."""

from argparse import ArgumentParser
from pathlib import Path
import shutil
import subprocess
import sys

SOURCE_SUFFIXES = {".jpeg", ".jpg", ".png"}


def run(command):
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode:
        if result.stdout:
            print(result.stdout, file=sys.stderr)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        result.check_returncode()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path("dist/assets/images"))
    parser.add_argument("--webp-quality", type=int, default=82)
    parser.add_argument("--avif-quality", type=int, default=50)
    args = parser.parse_args()

    if not args.directory.is_dir():
        parser.error(f"image directory does not exist: {args.directory}")
    missing = [tool for tool in ("cwebp", "avifenc") if not shutil.which(tool)]
    if missing:
        parser.error(f"missing required image encoder(s): {', '.join(missing)}")

    sources = sorted(path for path in args.directory.iterdir() if path.suffix.lower() in SOURCE_SUFFIXES)
    for source in sources:
        webp = source.with_suffix(".webp")
        avif = source.with_suffix(".avif")
        run(["cwebp", "-quiet", "-q", str(args.webp_quality), str(source), "-o", str(webp)])
        run(["avifenc", "-q", str(args.avif_quality), str(source), str(avif)])
        print(f"{source.name} -> {webp.name}, {avif.name}")
    print(f"Generated optimized variants for {len(sources)} image(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
