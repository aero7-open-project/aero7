#!/usr/bin/env python3
"""Verify one final Beta 2 ISO pair and create local website metadata."""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import re
import stat
import subprocess
import tempfile
from typing import Callable


IMAGE_NAME = re.compile(
    r"^aero7-beta2-(online|offline)-(\d{4}\.\d{2}\.\d{2})-x86_64\.iso$"
)
OUTPUT_NAMES = ("SHA256SUMS", "BETA2-ARTIFACTS.md")


def validate_image(path: Path, expected_variant: str) -> str:
    try:
        info = path.lstat()
    except FileNotFoundError as error:
        raise ValueError(f"Missing {expected_variant} image: {path}") from error
    if not stat.S_ISREG(info.st_mode) or path.is_symlink():
        raise ValueError(f"The {expected_variant} image must be a regular non-symlink file: {path}")
    match = IMAGE_NAME.fullmatch(path.name)
    if not match or match.group(1) != expected_variant:
        raise ValueError(
            f"The {expected_variant} image has an invalid final filename: {path.name}"
        )
    return match.group(2)


def digest(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def render_metadata(images: list[tuple[str, Path, str]], release_date: str) -> tuple[str, str]:
    checksum = "".join(f"{image_hash}  {path.name}\n" for _, path, image_hash in images)
    rows = "\n".join(
        f"| {variant.capitalize()} | `{path.name}` | {path.stat().st_size:,} | `{image_hash}` |"
        for variant, path, image_hash in images
    )
    markdown = f"""# Aero7 Beta 2 final artifact metadata

Generated from the locally verified final image pair dated {release_date.replace('.', '-')}.
This file records artifact identity only; it is not signing or publication approval.

| Variant | Filename | Exact bytes | SHA-256 |
| --- | --- | ---: | --- |
{rows}

The offline image is the recommended download. Final website HTTPS URLs, upload
verification, signing state and publication approval remain separate release gates.
"""
    return checksum, markdown


def write_new_file(directory: Path, name: str, content: str) -> None:
    target = directory / name
    temporary_name = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", encoding="utf-8", dir=directory, prefix=f".{name}.", delete=False
        ) as output:
            temporary_name = output.name
            output.write(content)
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary_name, 0o644)
        # Existing metadata is never replaced implicitly. The caller must choose
        # a clean output directory for a newly accepted pair.
        if target.exists() or target.is_symlink():
            raise ValueError(f"Refusing to replace existing release metadata: {target}")
        os.link(temporary_name, target)
    finally:
        if temporary_name:
            Path(temporary_name).unlink(missing_ok=True)


def finalize(
    online: Path,
    offline: Path,
    output_directory: Path,
    verifier: Callable[[Path], None],
) -> tuple[Path, Path]:
    online_date = validate_image(online, "online")
    offline_date = validate_image(offline, "offline")
    if online_date != offline_date:
        raise ValueError("Online and offline images must have the same release date")
    if os.path.samefile(online, offline):
        raise ValueError("Online and offline inputs resolve to the same file")

    if output_directory.exists() and not output_directory.is_dir():
        raise ValueError(f"Metadata output is not a directory: {output_directory}")
    output_directory.mkdir(mode=0o755, parents=False, exist_ok=True)
    for name in OUTPUT_NAMES:
        target = output_directory / name
        if target.exists() or target.is_symlink():
            raise ValueError(f"Refusing to replace existing release metadata: {target}")

    # Recommended/offline first in both verification output and website files.
    verifier(offline)
    verifier(online)
    images = [
        ("offline", offline, digest(offline)),
        ("online", online, digest(online)),
    ]
    checksums, artifacts = render_metadata(images, online_date)
    write_new_file(output_directory, OUTPUT_NAMES[0], checksums)
    try:
        write_new_file(output_directory, OUTPUT_NAMES[1], artifacts)
    except Exception:
        (output_directory / OUTPUT_NAMES[0]).unlink(missing_ok=True)
        raise
    return tuple(output_directory / name for name in OUTPUT_NAMES)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--online", type=Path, required=True)
    parser.add_argument("--offline", type=Path, required=True)
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[1]

    def verify(image: Path) -> None:
        subprocess.run(
            [project_root / "scripts/verify-release.sh", image],
            cwd=project_root,
            check=True,
        )

    try:
        outputs = finalize(args.online, args.offline, args.output_directory, verify)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Final artifact preparation failed: {error}", file=os.sys.stderr)
        return 1
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
