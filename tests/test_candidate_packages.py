import hashlib
import importlib.util
import io
import re
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location("candidate_packages", Path(__file__).resolve().parents[1] / "scripts/verify-candidate-packages.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class CandidatePackageTests(unittest.TestCase):
    def test_release_notes_match_metadata_and_optional_policy(self):
        notes = "## Current local candidate packages\n\n| `core` | `1-2` |\n| `extra` (optional) | `3-4` |\n\n## Later\n"
        checker.verify_release_notes(notes, [{"pkgname": "core", "pkgver": "1-2"},
                                             {"pkgname": "extra", "pkgver": "3-4"}], {"extra"})

    def test_release_notes_reject_stale_missing_and_extra_versions(self):
        identity = [{"pkgname": "core", "pkgver": "1-2"}]
        for table in ("| `core` | `1-1` |", "", "| `core` | `1-2` |\n| `old` | `1-1` |"):
            with self.subTest(table=table), self.assertRaisesRegex(ValueError, "versions differ"):
                checker.verify_release_notes("## Current local candidate packages\n" + table + "\n", identity, set())

    def test_release_notes_reject_duplicate_and_missing_table(self):
        identity = [{"pkgname": "core", "pkgver": "1-2"}]
        with self.assertRaisesRegex(ValueError, "Duplicate release-notes"):
            checker.verify_release_notes("## Current local candidate packages\n" + "| `core` | `1-2` |\n" * 2,
                                         identity, set())
        with self.assertRaisesRegex(ValueError, "missing"):
            checker.verify_release_notes("# Old release notes\n", identity, set())

    def test_release_notes_reject_wrong_optional_labels(self):
        identity = [{"pkgname": "vault", "pkgver": "1-7"}]
        for marker, optional in (("", {"vault"}), (" (optional)", set())):
            with self.subTest(marker=marker), self.assertRaisesRegex(ValueError, "optional package labels"):
                checker.verify_release_notes("## Current local candidate packages\n"
                                             + f"| `vault`{marker} | `1-7` |\n", identity, optional)

    def test_offline_repository_rejects_checksum_pinned_package_duplicates(self):
        local = [{"pkgname": "aero7-shell", "pkgver": "2-1"}]
        offline = [{"pkgname": "aero7-shell", "pkgver": "1-1"}]
        with self.assertRaisesRegex(ValueError, "duplicates checksum-pinned local packages"):
            checker.verify_distinct_package_sources(local, offline)
        checker.verify_distinct_package_sources(
            local, [{"pkgname": "dependency", "pkgver": "1-1"}]
        )

    def test_release_verifier_enforces_fresh_firewall_and_update_dependencies(self):
        root = Path(__file__).resolve().parents[1]
        verifier = (root / "scripts/verify-release.sh").read_text()
        # Execute the actual verifier's package-policy loops on small fixtures;
        # do not duplicate their required/excluded lists in a mock validator.
        loops = []
        for variable in ("required_system_backend", "excluded_target_package"):
            match = re.search(rf"^for {variable} in .*?^done$", verifier, re.M | re.S)
            self.assertIsNotNone(match, variable)
            loops.append(match.group())
        program = 'set -euo pipefail\nembedded_base_packages="$1"\n' + "\n".join(loops)
        current = (root / "config/base-packages.txt").read_text()
        fixtures = [("current", current, True), ("legacy UFW", current + "\nufw\n", False)]
        for name in ("firewalld", "pacman-contrib", "fakeroot", "libnotify", "lsof"):
            fixtures.append((f"missing {name}", "\n".join(
                line for line in current.splitlines() if line != name) + "\n", False))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "base-packages.txt"
            for label, body, accepted in fixtures:
                with self.subTest(label=label):
                    path.write_text(body)
                    result = subprocess.run(["bash", "-c", program, "verifier-policy", str(path)],
                                            text=True, capture_output=True)
                    self.assertEqual(result.returncode == 0, accepted, result.stderr)

    def test_archive_name_policy(self):
        for name in ("/etc/passwd", "usr/../etc/foo", "usr/share/icons/.git/config", "usr/share/sounds/.git", "usr/share/.svn/entries"):
            self.assertTrue(checker.forbidden_member(name), name)
        for name in (".PKGINFO", ".BUILDINFO", "usr/share/icons/theme/index.theme", "usr/share/doc/example.gitignore"):
            self.assertFalse(checker.forbidden_member(name), name)

    def archive(self, directory, names):
        data = io.BytesIO()
        with tarfile.open(fileobj=data, mode="w") as archive:
            for name, content in names.items():
                entry = tarfile.TarInfo(name)
                entry.size = len(content)
                archive.addfile(entry, io.BytesIO(content))
        path = Path(directory) / "fixture.pkg.tar.zst"
        subprocess.run(["zstd", "-q", "-o", str(path)], input=data.getvalue(), check=True)
        return path, hashlib.sha256(path.read_bytes()).hexdigest()

    @unittest.skipUnless(shutil.which("zstd"), "zstd required for package fixtures")
    def test_clean_archive_returns_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            path, digest = self.archive(directory, {".PKGINFO": b"pkgname = test\npkgver = 1-1\n", "usr/share/icons/theme/icon.svg": b"art"})
            self.assertEqual(checker.inspect_archive(path, digest), {"pkgname": "test", "pkgver": "1-1"})

    @unittest.skipUnless(shutil.which("zstd"), "zstd required for package fixtures")
    def test_git_metadata_rejected_even_with_correct_checksum(self):
        with tempfile.TemporaryDirectory() as directory:
            path, digest = self.archive(directory, {".PKGINFO": b"pkgname = test\npkgver = 1-1\n", "usr/share/icons/.git/config": b"checkout data"})
            with self.assertRaisesRegex(ValueError, "forbidden archive paths"):
                checker.inspect_archive(path, digest)

    @unittest.skipUnless(shutil.which("zstd"), "zstd required for package fixtures")
    def test_changed_archive_checksum_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path, _ = self.archive(directory, {".PKGINFO": b"pkgname = test\npkgver = 1-1\n"})
            with self.assertRaisesRegex(ValueError, "Checksum mismatch"):
                checker.inspect_archive(path, "0" * 64)

    def test_manifest_rejects_escape_and_duplicates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for body in ("0" * 64 + "  ../outside\n", ("0" * 64 + "  same.pkg\n") * 2):
                (root / "manifest").write_text(body)
                with self.assertRaises(ValueError):
                    checker.manifest(root, "manifest")


if __name__ == "__main__":
    unittest.main()
