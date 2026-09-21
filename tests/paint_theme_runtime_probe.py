#!/usr/bin/env python3
"""Compare existing and corrected theme files in isolated VM user directories.

Run inside the graphical user's systemd environment. No installed package or
user preference is replaced. The measured event is the compositor's first
toplevel configure, not a universal startup benchmark or first-paint guarantee.
"""

import hashlib
import json
import os
import re
import selectors
import shutil
import subprocess
import tempfile
import time
from pathlib import Path


def probe():
    source = Path("/usr/share/Kvantum/Windows7Aero")
    svg = (source / "Windows7Aero.svg").read_bytes()
    assert hashlib.sha256(svg).hexdigest() == "a5fe4339f0e51bf611a15cfa44b4a9347d3af12449824e77a43da939dd4b5561"
    corrected = svg.replace(b"#slider-normal-topleft-3\"", b"#slider-normal-topleft\"")
    corrected = corrected.replace(b"#slider-normal-topright-7\"", b"#slider-normal-topright\"")
    assert hashlib.sha256(corrected).hexdigest() == "43710cc09dc680f1f252003abf51c0c7a5c599b0666821545da258a2e03b0926"
    results = []
    for mode in ("baseline", "corrected"):
        with tempfile.TemporaryDirectory(prefix=f"aero7-paint-{mode}-") as directory:
            root = Path(directory)
            config = root / "config"
            theme = config / "Kvantum/Windows7Aero"
            theme.mkdir(parents=True)
            (theme / "Windows7Aero.svg").write_bytes(corrected if mode == "corrected" else svg)
            shutil.copy2(source / "Windows7Aero.kvconfig", theme)
            (config / "Kvantum/kvantum.kvconfig").write_text("[General]\ntheme=Windows7Aero\n")
            user_config = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config")))
            for name in ("kdeglobals", "kolourpaintrc"):
                if (user_config / name).is_file():
                    shutil.copy2(user_config / name, config / name)
            if mode == "corrected":
                original_icons = Path("/usr/share/icons/Windows 7 Aero")
                icons = root / "data/icons/Windows 7 Aero"
                icons.mkdir(parents=True)
                for child in original_icons.iterdir():
                    if child.name != "index.theme":
                        (icons / child.name).symlink_to(child)
                metadata = (original_icons / "index.theme").read_text()
                assert "Inherits=hicolor,oxygen-icons5,oxygen,breeze" in metadata
                (icons / "index.theme").write_text(metadata.replace("Inherits=hicolor,oxygen-icons5,oxygen,breeze", "Inherits=hicolor,breeze"))
            # Explicitly select the session's Kvantum style in both fixtures so
            # this comparison cannot drift to Qt's fallback style.
            environment = dict(os.environ, XDG_CONFIG_HOME=str(config), XDG_DATA_HOME=str(root / "data"),
                               XDG_CACHE_HOME=str(root / "cache"), WAYLAND_DEBUG="1", QT_STYLE_OVERRIDE="kvantum")
            start = time.monotonic()
            process = subprocess.Popen(["/usr/bin/kolourpaint"], env=environment,
                                       stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            lines = bytearray()
            configured = None
            try:
                with selectors.DefaultSelector() as selector:
                    selector.register(process.stderr, selectors.EVENT_READ)
                    while time.monotonic() - start < 20:
                        for key, _ in selector.select(0.2):
                            chunk = os.read(key.fileobj.fileno(), 65536)
                            if not chunk:
                                raise RuntimeError(f"{mode}: Paint exited before the observation completed")
                            lines.extend(chunk)
                            if configured is None and re.search(rb"xdg_toplevel[^\n]*\.configure\(", lines):
                                configured = time.monotonic() - start
                        if configured is not None and time.monotonic() - start > configured + 3:
                            break
            finally:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
                process.stderr.close()
            # KDE sends Qt warnings directly to journald, not necessarily to
            # stderr. Read both sinks and filter by this exact child PID/boot.
            journal = subprocess.run(["journalctl", "--user", "-b", "--no-pager", "-o", "cat", f"_PID={process.pid}"],
                                     check=True, capture_output=True, text=True, timeout=10).stdout
            warnings = [line for line in (lines.decode(errors="replace") + journal).splitlines()
                        if "is undefined!" in line or "oxygen-icons5" in line]
            result = dict(mode=mode, first_toplevel_configure_seconds=configured, theme_warnings=len(warnings),
                          svg_sha256=hashlib.sha256((theme / "Windows7Aero.svg").read_bytes()).hexdigest())
            print(json.dumps(result), flush=True)
            assert configured is not None, f"{mode}: no compositor configure within 20 seconds"
            if mode == "baseline":
                assert warnings, "baseline did not reproduce the known warnings"
            else:
                assert not warnings, warnings
            results.append(result)
        assert not root.exists()
    print("PASS both isolated launches configured; corrected theme emitted no targeted warnings; fixtures removed", flush=True)


if __name__ == "__main__":
    try:
        probe()
    except Exception as error:
        print(f"FAIL {type(error).__name__}: {error}", flush=True)
        raise SystemExit(1)
