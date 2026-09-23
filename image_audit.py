#!/usr/bin/env python3
"""Check the dimensions and payload budget of generated static-site images."""

from argparse import ArgumentParser
from pathlib import Path
import subprocess
import sys

IMAGE_SUFFIXES = {".avif", ".jpeg", ".jpg", ".png", ".webp"}
ACTIVE_SUFFIXES = {".jpeg", ".jpg", ".png"}


def dimensions(image):
    result = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(image)],
        check=True,
        capture_output=True,
        text=True,
    )
    values = {}
    for line in result.stdout.splitlines():
        key, separator, value = line.partition(":")
        if separator and key.strip() in {"pixelWidth", "pixelHeight"}:
            values[key.strip()] = int(value.strip())
    return values["pixelWidth"], values["pixelHeight"]


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--directory", type=Path, default=Path("dist/assets/images"))
    parser.add_argument("--max-dimension", type=int, default=2560)
    parser.add_argument("--max-file-bytes", type=int, default=2621440)
    parser.add_argument("--max-total-bytes", type=int, default=8388608)
    args = parser.parse_args()

    if not args.directory.is_dir():
        parser.error(f"image directory does not exist: {args.directory}")

    images = sorted(path for path in args.directory.iterdir() if path.suffix.lower() in IMAGE_SUFFIXES)
    total = 0
    failures = []
    print("File                              Dimensions       Size")
    print("-" * 62)
    for image in images:
        size = image.stat().st_size
        if image.suffix.lower() in ACTIVE_SUFFIXES:
            total += size
        try:
            width, height = dimensions(image)
        except (KeyError, subprocess.CalledProcessError) as error:
            failures.append(f"{image.name}: unable to read dimensions ({error})")
            continue
        print(f"{image.name:<33} {width:>4} x {height:<4} {size / 1024:>8.1f} KiB")
        if max(width, height) > args.max_dimension:
            failures.append(
                f"{image.name}: {width}x{height} exceeds {args.max_dimension}px maximum edge"
            )
        if size > args.max_file_bytes:
            failures.append(
                f"{image.name}: {size} bytes exceeds {args.max_file_bytes} bytes per-image budget"
            )
    print("-" * 62)
    print(
        f"{len(images)} image files; active-format total {total / 1024 / 1024:.2f} MiB"
    )
    if total > args.max_total_bytes:
        failures.append(f"total: {total} bytes exceeds {args.max_total_bytes} bytes budget")
    if failures:
        print("\nImage budget failures:", file=sys.stderr)
        print("\n".join(f"- {failure}" for failure in failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
