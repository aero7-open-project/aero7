#!/usr/bin/python3
"""Explicit QA-only backend: fail one save, then exec normal Spectacle on retry.

Set AERO7_QA_FAIL_ONCE_STATE to a new marker inside the test user's runtime
directory. Used only by a transient test Snipping Tool service, never installed
or selected by the production desktop.
"""

import os
from pathlib import Path
import sys


def main():
    marker = Path(os.environ["AERO7_QA_FAIL_ONCE_STATE"])
    runtime = Path(os.environ["XDG_RUNTIME_DIR"]).resolve(strict=True)
    if marker.parent.resolve(strict=True) != runtime:
        raise ValueError("The QA marker must be directly inside XDG_RUNTIME_DIR")
    arguments = sys.argv[1:]
    # Validate before creating the marker; malformed fixture invocations must
    # not accidentally skip the intended error on the following capture.
    output = arguments.index("--output") + 1
    if output >= len(arguments):
        raise ValueError("Missing --output value")
    try:
        marker_fd = os.open(marker, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        pass
    else:
        os.close(marker_fd)
        arguments[output] = "/proc/aero7-qa-failed-screenshot.png"
    os.execv("/usr/bin/spectacle", ["spectacle", *arguments])


if __name__ == "__main__":
    main()
