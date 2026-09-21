import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("elf_needed", ROOT / "scripts/compare-elf-needed.py")
elf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(elf)


class ElfNeededTests(unittest.TestCase):
    def test_parses_sorts_and_deduplicates_without_executing_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "library").write_bytes(b"\x7fELFfixture")
            (root / "text").write_text("not a binary")
            (root / "link").symlink_to(root / "library")
            output = "\n".join(
                f" 0x01 (NEEDED) Shared library: [{name}]"
                for name in ["libz.so.1", "liba.so.0", "libz.so.1"]
            )
            with patch.object(elf.subprocess, "run", return_value=SimpleNamespace(stdout=output)) as run:
                self.assertEqual(elf.requirements(root), {"library": ["liba.so.0", "libz.so.1"]})
                self.assertEqual(run.call_count, 1)
                self.assertEqual(run.call_args.args[0][0], "readelf")
                self.assertTrue(run.call_args.kwargs["check"])

    def test_empty_tree_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                elf.requirements(Path(directory))

    def test_malformed_elf_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "bad").write_bytes(b"\x7fELFbad")
            with patch.object(elf.subprocess, "run", side_effect=subprocess.CalledProcessError(1, "readelf")):
                with self.assertRaises(subprocess.CalledProcessError):
                    elf.requirements(root)

    def compare(self, baseline, candidate):
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            with patch("sys.argv", ["compare-elf-needed.py", directory, directory]):
                with patch.object(elf, "requirements", side_effect=[baseline, candidate]):
                    with contextlib.redirect_stdout(output):
                        code = elf.main()
        return code, json.loads(output.getvalue())

    def test_identical_requirements_pass(self):
        code, report = self.compare({"bin/a": ["libc.so.6"]}, {"bin/a": ["libc.so.6"]})
        self.assertEqual(code, 0)
        self.assertEqual(report["changed"], {})

    def test_new_optional_dependency_fails(self):
        code, report = self.compare({"lib/a": ["libc.so.6"]}, {"lib/a": ["libc.so.6", "libflatpak.so.0"]})
        self.assertEqual(code, 1)
        self.assertIn("lib/a", report["changed"])

    def test_added_elf_fails(self):
        code, report = self.compare({"bin/a": []}, {"bin/a": [], "bin/b": []})
        self.assertEqual(code, 1)
        self.assertIsNone(report["changed"]["bin/b"]["baseline"])

    def test_removed_elf_fails(self):
        code, report = self.compare({"bin/a": [], "bin/b": []}, {"bin/a": []})
        self.assertEqual(code, 1)
        self.assertIsNone(report["changed"]["bin/b"]["candidate"])


if __name__ == "__main__":
    unittest.main()
