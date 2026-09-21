#!/usr/bin/env python3
"""Read-only runtime QA apart from an automatically removed temporary target.

Run with configure_target_preferences injected from the exact candidate source.
Does not replace any guest configuration, package, service or ISO. This is not
fresh-install acceptance and does not test translated custom application text.
"""

import os
import subprocess
import tempfile
from pathlib import Path


def probe():
    with tempfile.TemporaryDirectory(prefix="aero7-regional-qa-") as directory:
        target = Path(directory)
        configure_target_preferences(target, {
            "language": "Nederlands", "time_format": "Nederlands (Nederland)", "keyboard": "Dutch"})
        (target / "home").mkdir()
        environment = dict(os.environ, HOME=str(target / "home"), XDG_CONFIG_HOME=str(target / "home/.config"),
                           XDG_CONFIG_DIRS=str(target / "etc/xdg"), LC_ALL="C.UTF-8", LANGUAGE="C")
        def command(argv, env=environment):
            result = subprocess.run(argv, env=env, check=True, text=True, capture_output=True, timeout=60)
            assert not result.stderr.strip(), result.stderr
            return result.stdout.strip()
        for filename, group, key, expected in (
                ("kxkbrc", "Layout", "LayoutList", "nl"),
                ("plasma-localerc", "Formats", "LANG", "nl_NL.UTF-8"),
                ("plasma-localerc", "Formats", "LC_TIME", "nl_NL.UTF-8"),
                ("plasma-localerc", "Translations", "LANGUAGE", "nl:en_US")):
            actual = command(["kreadconfig6", "--file", filename, "--group", group, "--key", key])
            assert actual == expected, (filename, key, actual, expected)
            print(f"PASS KDE system default {filename}/{group}/{key}={actual}", flush=True)
        for layout in ("us", "nl"):
            command(["xkbcli", "compile-keymap", "--layout", layout, "--test"])
            assert Path(f"/usr/share/kbd/keymaps/i386/qwerty/{layout}.map.gz").is_file()
            print(f"PASS compiled XKB layout and installed console map: {layout}", flush=True)
        locale_root = target / "locales"
        locale_root.mkdir()
        command(["localedef", "--no-archive", "-i", "nl_NL", "-f", "UTF-8", str(locale_root / "nl_NL.UTF-8")])
        dutch = dict(environment, LOCPATH=str(locale_root), LC_ALL="nl_NL.UTF-8", LANGUAGE="nl")
        decimal = command(["locale", "decimal_point"], dutch)
        monday = command(["date", "--date=2026-09-07", "+%A"], dutch)
        assert decimal == ",", decimal
        assert monday == "maandag", monday
        print(f"PASS isolated Dutch locale: decimal={decimal} weekday={monday}", flush=True)
    assert not target.exists()
    print("PASS temporary target removed; installed settings unchanged", flush=True)


if __name__ == "__main__":
    probe()
