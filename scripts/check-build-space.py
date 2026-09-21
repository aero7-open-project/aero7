#!/usr/bin/env python3
"""Read-only, conservative capacity check before Archiso staging is changed."""

import argparse
import os
from pathlib import Path
import stat
import sys


GIB = 1024 ** 3


def profile_bytes(profile: Path) -> int:
    if not profile.is_dir():
        raise ValueError(f"Prepared profile is missing: {profile}")
    total = 0

    def walk_error(error):
        raise error

    # Count apparent bytes, including sparse files. Do not follow symlinks into
    # unrelated directories or count only currently allocated filesystem blocks.
    for directory, _, files in os.walk(profile, followlinks=False, onerror=walk_error):
        for name in files:
            info = (Path(directory) / name).lstat()
            if stat.S_ISREG(info.st_mode):
                total += info.st_size
    return total


def existing_directory(path: Path) -> Path:
    path = path.resolve()
    while not path.exists():
        if path == path.parent:
            raise ValueError(f"Cannot find filesystem for {path}")
        path = path.parent
    if not path.is_dir():
        raise ValueError(f"Not a directory: {path}")
    return path


def filesystem(path: Path) -> tuple[int, int]:
    directory = existing_directory(path)
    info = directory.stat()
    usage = os.statvfs(directory)
    # Use unprivileged-available bytes even when the build itself runs as root:
    # reserved blocks must not be consumed to keep an ISO build alive.
    return info.st_dev, usage.f_bavail * usage.f_frsize


def assess(size: int, work: tuple[int, int], output: tuple[int, int]) -> list[str]:
    if size < 0:
        raise ValueError("Profile size cannot be negative")
    # Live root/package-cache/headroom plus profile copies in the live root,
    # SquashFS and staged ISO. This is a conservative floor, not a prediction or
    # a guarantee against concurrent writers or future package growth.
    required_work = 16 * GIB + 3 * size
    requirements = [("build workspace", work[1], required_work)]
    if work[0] != output[0]:
        # Across filesystems mv copies before unlinking the staged image.
        requirements.append(("ISO output", output[1], 4 * GIB + size))
    errors = []
    for label, available, required in requirements:
        if available < required:
            errors.append(f"{label}: {available / GIB:.1f} GiB available; "
                          f"at least {required / GIB:.1f} GiB required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        size = profile_bytes(args.profile)
        errors = assess(size, filesystem(args.work), filesystem(args.output))
    except (OSError, ValueError) as error:
        print(f"Cannot verify build capacity: {error}", file=sys.stderr)
        return 1
    if errors:
        print("Insufficient free space for ISO staging:\n  " + "\n  ".join(errors),
              file=sys.stderr)
        print("Stopped before build-tree cleanup. Preserve existing images and logs; "
              "free reviewed disposable data or use a larger build filesystem.",
              file=sys.stderr)
        return 1
    print(f"Build-space preflight passed (profile {size / GIB:.2f} GiB).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
