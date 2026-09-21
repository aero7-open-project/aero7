#!/usr/bin/env python3
"""Compare direct ELF requirements in two trusted, extracted package trees.

This catches accidental optional-library autodetection when rebuilding an
otherwise unchanged package. It does not establish target dependency closure
or ABI compatibility; those still require isolated build and guest checks.
It never executes the inspected binaries (unlike a loader-based ldd check).
"""

import argparse
import json
from pathlib import Path
import re
import subprocess


def requirements(root: Path) -> dict[str, list[str]]:
    result = {}
    for path in sorted(root.rglob("*")):
        if path.is_symlink() or not path.is_file():
            continue
        with path.open("rb") as stream:
            if stream.read(4) != b"\x7fELF":
                continue
        dynamic = subprocess.run(
            ["readelf", "--dynamic", "--wide", str(path)],
            check=True, capture_output=True, text=True,
            env={"PATH": "/usr/bin:/bin", "LC_ALL": "C"},
        ).stdout
        result[str(path.relative_to(root))] = sorted(set(
            re.findall(r"\(NEEDED\).*?Shared library: \[([^\]]+)\]", dynamic)
        ))
    if not result:
        raise ValueError(f"No ELF files in {root}")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    baseline = requirements(args.baseline.resolve(strict=True))
    candidate = requirements(args.candidate.resolve(strict=True))
    changes = {
        path: {"baseline": baseline.get(path), "candidate": candidate.get(path)}
        for path in sorted(baseline.keys() | candidate.keys())
        if baseline.get(path) != candidate.get(path)
    }
    print(json.dumps({
        "baseline_elf_count": len(baseline),
        "candidate_elf_count": len(candidate),
        "changed": changes,
    }, indent=2))
    return int(bool(changes))


if __name__ == "__main__":
    raise SystemExit(main())
