#!/usr/bin/env python3
"""Check the real theme archive and repeat-setup behavior in an isolated tree."""

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "backend"))
from aero7_install_backend import brand_plasma_lock_screen  # noqa: E402


def main(package: Path) -> None:
    def read(entry: str) -> bytes:
        return subprocess.check_output(["bsdtar", "-xOf", str(package), entry])

    info = read(".PKGINFO").decode()
    assert "pkgname = aerothemeplasma-desktop-git\n" in info
    logo = (PROJECT / "installer/assets/aero7-sddm-branding.png").read_bytes()
    assert hashlib.sha256(logo).hexdigest() == "d45164d6d67f2d8ccae63c4fd83bd0dd73e05808f3c8cd739c4850b5680d4982"
    sddm = "usr/share/sddm/themes/sddm-theme-mod/"
    shell = "usr/share/plasma/shells/io.gitgud.wackyideas.desktop/"
    for name in ("background", "default-background", "preview.png"):
        assert hashlib.sha256(read(sddm + name)).hexdigest() == "65e825c2dcc1b0c80d14896a6108199d825f8dc7b44724f22fe19d8b308fb7e7", name
    entries = subprocess.check_output(["bsdtar", "-tf", str(package)]).decode().splitlines()
    assert sddm + "bgtexture.jpg" not in entries, "Do not seize setup-owned bgtexture.jpg on upgrade"
    assert read(sddm + "Assets/aero7-branding-r3.png") == logo
    assert read(shell + "contents/images/branding.png") == logo
    assert read("usr/share/plasma/look-and-feel/authui7/contents/images/aero7-package-branding.png") == logo
    assert b"Assets/aero7-branding-r3.png" in read(sddm + "Main.qml")
    assert b"Image.PreserveAspectFit" in read(shell + "contents/lockscreen/AuthUI.qml")

    with tempfile.TemporaryDirectory(prefix="aero7-theme-branding-") as temporary:
        root = Path(temporary)
        files = []
        for name in ("contents/lockscreen/AuthUI.qml", "contents/components/GenericButton.qml", "contents/images/branding.png"):
            path = root / "shells/io.gitgud.wackyideas.desktop" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(read(shell + name))
            files.append(path)
        source = root / "approved-logo.png"
        source.write_bytes(logo)
        before = {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files}
        for _ in range(2):
            result = brand_plasma_lock_screen(root / "shells", source)
            assert result == [root / "shells/io.gitgud.wackyideas.desktop"]
            assert before == {path: (path.read_bytes(), path.stat().st_mtime_ns) for path in files}
    print("THEME_PACKAGE_BRANDING_AND_REPEAT_SETUP_VERIFIED_NOT_VM_ACCEPTANCE")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(strict=True))
