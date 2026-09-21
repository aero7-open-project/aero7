import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "finalize_release_artifacts", ROOT / "scripts/finalize-release-artifacts.py"
)
artifacts = importlib.util.module_from_spec(spec)
spec.loader.exec_module(artifacts)


class FinalizeReleaseArtifactsTests(unittest.TestCase):
    def images(self, root: Path, online_date="2026.09.22", offline_date="2026.09.22"):
        online = root / f"aero7-beta2-online-{online_date}-x86_64.iso"
        offline = root / f"aero7-beta2-offline-{offline_date}-x86_64.iso"
        online.write_bytes(b"online image")
        offline.write_bytes(b"offline image")
        return online, offline

    def test_writes_offline_first_checksums_and_artifact_table_after_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            online, offline = self.images(root)
            verified = []
            outputs = artifacts.finalize(
                online, offline, root / "metadata", lambda path: verified.append(path)
            )
            self.assertEqual(verified, [offline, online])
            self.assertEqual([path.name for path in outputs], list(artifacts.OUTPUT_NAMES))
            checksums = outputs[0].read_text().splitlines()
            self.assertTrue(checksums[0].endswith(f"  {offline.name}"))
            self.assertTrue(checksums[1].endswith(f"  {online.name}"))
            table = outputs[1].read_text()
            self.assertIn("2026-09-22", table)
            self.assertIn(f"| Offline | `{offline.name}` | 13 |", table)
            self.assertIn(f"| Online | `{online.name}` | 12 |", table)
            self.assertIn("not signing or publication approval", table)

    def test_verifier_failure_creates_no_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            online, offline = self.images(root)
            output = root / "metadata"

            def reject(_path):
                raise ValueError("bad image")

            with self.assertRaisesRegex(ValueError, "bad image"):
                artifacts.finalize(online, offline, output, reject)
            self.assertEqual(list(output.iterdir()), [])

    def test_rejects_mismatched_dates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            online, offline = self.images(root, offline_date="2026.09.23")
            with self.assertRaisesRegex(ValueError, "same release date"):
                artifacts.finalize(online, offline, root / "metadata", lambda _path: None)

    def test_rejects_wrong_variant_name_and_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            online, offline = self.images(root)
            with self.assertRaisesRegex(ValueError, "invalid final filename"):
                artifacts.validate_image(online, "offline")
            linked = root / "aero7-beta2-online-2026.09.23-x86_64.iso"
            linked.symlink_to(online)
            with self.assertRaisesRegex(ValueError, "non-symlink"):
                artifacts.validate_image(linked, "online")

    def test_refuses_existing_metadata_before_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            online, offline = self.images(root)
            output = root / "metadata"
            output.mkdir()
            (output / "SHA256SUMS").write_text("old")
            calls = []
            with self.assertRaisesRegex(ValueError, "replace existing"):
                artifacts.finalize(online, offline, output, lambda path: calls.append(path))
            self.assertEqual(calls, [])
            self.assertEqual((output / "SHA256SUMS").read_text(), "old")


if __name__ == "__main__":
    unittest.main()
