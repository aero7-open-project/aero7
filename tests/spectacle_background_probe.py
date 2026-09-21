#!/usr/bin/env python3
"""Opt-in Spectacle save/error probe; run as the test VM's graphical user.

Captures the VM display to a new private temporary directory. The directory is
retained for inspection. Never run against a personal desktop without consent.
An exit timeout is a failure, not a successful error-reporting result.
"""

import argparse
import json
import os
from pathlib import Path
import signal
import struct
import subprocess
import tempfile
import time


def run_capture(binary, output, new_instance):
    command = [str(binary), "--desktopfile", "org.kde.spectacle", "--fullscreen",
               "--background", "--nonotify", "--output", str(output)]
    if new_instance:
        command.append("--new-instance")
    start = time.monotonic()
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=10)
        result = {"exit": process.returncode, "timeout": False}
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            stdout, stderr = process.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            stdout, stderr = process.communicate()
        result = {"exit": process.returncode, "timeout": True}
    result.update(seconds=round(time.monotonic() - start, 3),
                  stdout=stdout.decode(errors="replace"),
                  stderr=stderr.decode(errors="replace"))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    args = parser.parse_args()
    if not (os.environ.get("WAYLAND_DISPLAY") or os.environ.get("DISPLAY")):
        parser.error("Run inside the test VM's active graphical session")
    binary = args.binary.resolve(strict=True)
    root = Path(tempfile.mkdtemp(prefix="aero7-spectacle-probe-"))
    report = {"binary": str(binary), "evidence": str(root), "cases": []}
    for new_instance in (True, False):
        mode = "new-instance" if new_instance else "unique-instance"
        output = root / f"{mode}.png"
        case = run_capture(binary, output, new_instance)
        signature = output.read_bytes()[:24] if output.is_file() else b""
        png = len(signature) == 24 and signature[:16] == b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR"
        dimensions = struct.unpack(">II", signature[16:24]) if png else (0, 0)
        case.update(name=f"{mode}-save", dimensions=dimensions,
                    passed=not case["timeout"] and case["exit"] == 0
                    and all(dimensions))
        report["cases"].append(case)
        capture_works = case["passed"]
        # /proc cannot contain a newly created regular image. Use a unique name
        # and do not change permissions or remove any existing path to force failure.
        invalid = Path("/proc") / f"{root.name}-{mode}.png"
        if invalid.exists():
            raise RuntimeError(f"Unexpected pre-existing probe target: {invalid}")
        case = run_capture(binary, invalid, new_instance)
        case.update(name=f"{mode}-save-error",
                    capture_precondition_passed=capture_works,
                    passed=capture_works and not case["timeout"] and case["exit"] == 1
                    and not invalid.exists())
        report["cases"].append(case)
    report["passed"] = all(case["passed"] for case in report["cases"])
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
