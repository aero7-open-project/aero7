import importlib.util
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_space", ROOT / "scripts/check-build-space.py")
space = importlib.util.module_from_spec(spec)
spec.loader.exec_module(space)


class BuildSpaceTests(unittest.TestCase):
    def test_same_filesystem_does_not_double_count_move(self):
        self.assertEqual(space.assess(space.GIB, (1, 19 * space.GIB), (1, 19 * space.GIB)), [])

    def test_work_boundary_rejects_one_byte_short(self):
        self.assertEqual(len(space.assess(space.GIB, (1, 19 * space.GIB - 1), (1, 19 * space.GIB - 1))), 1)

    def test_separate_output_needs_copy_capacity(self):
        errors = space.assess(space.GIB, (1, 30 * space.GIB), (2, 5 * space.GIB - 1))
        self.assertEqual(len(errors), 1)
        self.assertIn("ISO output", errors[0])

    def test_separate_output_exact_capacity_passes(self):
        self.assertEqual(space.assess(space.GIB, (1, 19 * space.GIB), (2, 5 * space.GIB)), [])

    def test_both_filesystems_report_shortage(self):
        self.assertEqual(len(space.assess(space.GIB, (1, 0), (2, 0))), 2)

    def test_empty_profile_still_requires_live_root_headroom(self):
        self.assertTrue(space.assess(0, (1, 15 * space.GIB), (1, 15 * space.GIB)))

    def test_negative_size_rejected(self):
        with self.assertRaises(ValueError):
            space.assess(-1, (1, 0), (1, 0))

    def test_profile_counts_apparent_bytes_without_following_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            profile = root / "profile"
            profile.mkdir()
            (profile / "payload").write_bytes(b"12345")
            outside = root / "outside"
            outside.mkdir()
            (outside / "not-payload").write_bytes(b"abcdef")
            (profile / "linked-dir").symlink_to(outside, target_is_directory=True)
            (profile / "linked-file").symlink_to(outside / "not-payload")
            self.assertEqual(space.profile_bytes(profile), 5)

    def test_missing_profile_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                space.profile_bytes(Path(directory) / "absent")

    def test_missing_output_uses_nearest_existing_directory_without_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = root / "not-created" / "out"
            self.assertEqual(space.existing_directory(target), root.resolve())
            self.assertFalse(target.parent.exists())

    def test_uses_available_not_root_reserved_blocks(self):
        with tempfile.TemporaryDirectory() as directory:
            usage = SimpleNamespace(f_bavail=2, f_bfree=100, f_frsize=4096)
            with patch.object(space.os, "statvfs", return_value=usage):
                self.assertEqual(space.filesystem(Path(directory))[1], 8192)

    def test_space_check_precedes_any_build_tree_removal(self):
        builder = (ROOT / "scripts/build-iso.sh").read_text()
        check = builder.index('"$project_root/scripts/check-build-space.py"')
        self.assertLess(check, builder.index('rm -rf --one-file-system'))


if __name__ == "__main__":
    unittest.main()
