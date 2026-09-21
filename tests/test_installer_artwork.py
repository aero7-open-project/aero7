"""Keep the two replacement icons byte-identical to the selected icon pack."""

import hashlib
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallerArtworkTests(unittest.TestCase):
    def test_icons_and_notices_are_unchanged_package_copies(self):
        selected = [line.split(maxsplit=1) for line in
                    (ROOT / "config/beta2-local-packages.sha256").read_text().splitlines()
                    if "/aerothemeplasma-icons-git-" in line]
        self.assertEqual(len(selected), 1)
        package_hash, package_name = selected[0]
        package = ROOT / package_name
        self.assertEqual(hashlib.sha256(package.read_bytes()).hexdigest(), package_hash)
        sources = {
            "installer/assets/icons/check-green.png":
                "usr/share/icons/Windows 7 Aero/emblems/32/emblem-default.png",
            "installer/assets/icons/recycle-bin.png":
                "usr/share/icons/Windows 7 Aero/places/256/user-trash.png",
            "third_party/AeroThemePlasma-Icons-LICENSE":
                "usr/share/licenses/aerothemeplasma-icons-git/LICENSE",
            "third_party/AeroThemePlasma-Icons-NOTICE":
                "usr/share/licenses/aerothemeplasma-icons-git/README.md",
        }
        pinned = {path: digest for digest, path in
                  (line.split(maxsplit=1) for line in
                   (ROOT / "config/installer-icons.sha256").read_text().splitlines())}
        self.assertEqual(set(pinned), set(sources))
        for destination, member in sources.items():
            with self.subTest(destination=destination):
                original = subprocess.run(["bsdtar", "-xOf", str(package), member],
                                          capture_output=True, check=True).stdout
                copied = (ROOT / destination).read_bytes()
                self.assertEqual(copied, original)
                self.assertEqual(hashlib.sha256(copied).hexdigest(), pinned[destination])

    def test_replacement_resources_are_used_and_old_svgs_retired(self):
        cmake = (ROOT / "installer/CMakeLists.txt").read_text()
        for name, screen in (("check-green", "ProgressScreen"), ("recycle-bin", "DesktopScreen")):
            with self.subTest(name=name):
                self.assertIn(f"assets/icons/{name}.png", cmake)
                self.assertIn(f"qrc:/assets/icons/{name}.png",
                              (ROOT / f"installer/qml/screens/{screen}.qml").read_text())
                self.assertNotIn(f"assets/icons/{name}.svg", cmake)
                self.assertFalse((ROOT / f"installer/assets/icons/{name}.svg").exists())
        self.assertIn("../third_party/AeroThemePlasma-Icons-LICENSE", cmake)
        self.assertIn("../third_party/AeroThemePlasma-Icons-NOTICE", cmake)


if __name__ == "__main__":
    unittest.main()
