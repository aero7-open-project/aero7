#!/usr/bin/env python3
"""Setup preference regressions; all target writes stay in temporary fixtures."""

import itertools
import sys
import tempfile
import unittest
from contextlib import ExitStack, nullcontext
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
import aero7_install_backend as backend


class InstallPreferencesTest(unittest.TestCase):
    languages = {"English": "en_US.UTF-8", "Nederlands": "nl_NL.UTF-8"}
    regions = {"English (United States)": "en_US.UTF-8", "Nederlands (Nederland)": "nl_NL.UTF-8"}
    keyboards = {"US": "us", "Dutch": "nl"}

    def test_legacy_plans_keep_english_us_defaults(self):
        self.assertEqual(backend.install_preferences({}), {
            "language": "en_US.UTF-8", "time_format": "en_US.UTF-8", "keyboard": "us"})

    def test_all_eight_independent_combinations(self):
        for language, region, keyboard in itertools.product(self.languages, self.regions, self.keyboards):
            plan = dict(language=language, time_format=region, keyboard=keyboard)
            with self.subTest(**plan), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                backend.configure_target_preferences(target, plan)
                lang, loc, keymap = self.languages[language], self.regions[region], self.keyboards[keyboard]
                expected = f"LANG={lang}\n" + "".join(
                    f"{key}={loc}\n" for key in ("LC_TIME", "LC_NUMERIC", "LC_MONETARY", "LC_MEASUREMENT", "LC_PAPER"))
                self.assertEqual((target / "etc/locale.conf").read_text(), expected)
                self.assertEqual((target / "etc/vconsole.conf").read_text(), f"KEYMAP={keymap}\n")
                self.assertIn(f"LayoutList={keymap}\n", (target / "etc/xdg/kxkbrc").read_text())
                translation = "nl:en_US" if language == "Nederlands" else "en_US"
                self.assertEqual((target / "etc/xdg/plasma-localerc").read_text(),
                                 "[Formats]\n" + expected + f"\n[Translations]\nLANGUAGE={translation}\n")
                self.assertIn(f'Option "XkbLayout" "{keymap}"',
                              (target / "etc/X11/xorg.conf.d/00-keyboard.conf").read_text())
                self.assertEqual((target / "etc/systemd/system/aero7-oobe.service.d/20-regional-settings.conf").read_text(),
                                 "[Service]\nEnvironmentFile=/etc/locale.conf\n" + f"Environment=XKB_DEFAULT_LAYOUT={keymap}\n")
                before = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob("*") if p.is_file()}
                backend.configure_target_preferences(target, plan)
                after = {str(p.relative_to(target)): p.read_bytes() for p in target.rglob("*") if p.is_file()}
                self.assertEqual(before, after)

    def test_invalid_choices_reject_before_any_target_writes(self):
        for key, value in itertools.product(("language", "time_format", "keyboard"),
                                            (None, [], {}, 1, "", "unknown", "US\nINJECTED=yes")):
            with self.subTest(key=key, value=value), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                with self.assertRaisesRegex(backend.SafetyError, f"unsupported setup preference: {key}"):
                    backend.configure_target_preferences(target, {key: value})
                self.assertEqual(list(target.iterdir()), [])

    def test_invalid_preference_rejects_before_disk_or_network_work(self):
        with patch.object(backend, "enforce_execution_gate"), \
             patch.object(backend, "query_lsblk") as disks, \
             patch.object(backend, "ensure_install_network") as network, \
             patch.object(backend, "CommandRunner") as runner:
            with self.assertRaisesRegex(backend.SafetyError, "keyboard"):
                backend.install({"device": "/dev/never-touch", "keyboard": "invalid"}, "/dev/never-touch")
            disks.assert_not_called()
            network.assert_not_called()
            runner.assert_not_called()

    def test_locale_generation_preserves_existing_entries_and_is_idempotent(self):
        for language, region in itertools.product(self.languages, self.regions):
            with self.subTest(language=language, region=region), tempfile.TemporaryDirectory() as directory:
                target = Path(directory)
                (target / "etc").mkdir()
                locale_file = target / "etc/locale.gen"
                locale_file.write_text("# retained comment\nde_DE.UTF-8 UTF-8\n#en_US.UTF-8 UTF-8\n# nl_NL.UTF-8 UTF-8\n")
                plan = dict(language=language, time_format=region)
                runner = Mock()
                backend.generate_target_locales(target, plan, runner)
                first = locale_file.read_text()
                backend.generate_target_locales(target, plan, runner)
                self.assertEqual(locale_file.read_text(), first)
                self.assertTrue(first.startswith("# retained comment\nde_DE.UTF-8 UTF-8\n"))
                enabled = {line for line in first.splitlines() if not line.startswith("#")}
                self.assertEqual(enabled, {"de_DE.UTF-8 UTF-8", self.languages[language] + " UTF-8", self.regions[region] + " UTF-8"})
                runner.run.assert_called_with(["arch-chroot", str(target), "locale-gen"])
                for entry in enabled:
                    self.assertEqual(first.splitlines().count(entry), 1)

    def test_locale_generation_appends_missing_definitions(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            (target / "etc").mkdir()
            (target / "etc/locale.gen").write_text("# existing\n")
            backend.generate_target_locales(target, {"language": "Nederlands"}, Mock())
            self.assertEqual((target / "etc/locale.gen").read_text(),
                             "# existing\nen_US.UTF-8 UTF-8\nnl_NL.UTF-8 UTF-8\n")

    def test_preferences_exist_before_package_hooks_for_both_variants(self):
        # Exercise the real install ordering, but never run a real disk command.
        class ReachedPackageInstall(Exception):
            pass

        for variant in ("online", "offline"):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as directory, ExitStack() as stack:
                target = Path(directory) / "target"
                runner = Mock()
                runner.progress_heartbeat.side_effect = lambda *args: nullcontext()
                def run(argv, **kwargs):
                    if argv[0] == "pacstrap":
                        self.assertEqual((target / "etc/vconsole.conf").read_text(), "KEYMAP=nl\n")
                        self.assertIn("LANG=nl_NL.UTF-8\n", (target / "etc/locale.conf").read_text())
                        self.assertIn("LC_TIME=en_US.UTF-8\n", (target / "etc/locale.conf").read_text())
                        raise ReachedPackageInstall()
                runner.run.side_effect = run
                for name in ("enforce_execution_gate", "validate_plan", "ensure_install_network",
                             "ensure_install_tools", "wait_for_partitions", "preserve_live_install_logs", "event"):
                    stack.enter_context(patch.object(backend, name))
                for name, value in (("TARGET_ROOT", target), ("INSTALLER_LOG", Path(directory) / "install.log")):
                    stack.enter_context(patch.object(backend, name, value))
                for name, value in (("query_lsblk", []), ("find_disk", {}), ("live_sources", set()),
                                    ("install_variant", variant), ("verified_offline_package_files", []),
                                    ("CommandRunner", runner)):
                    stack.enter_context(patch.object(backend, name, return_value=value))
                stack.enter_context(patch.object(backend.subprocess, "run"))
                original_read = Path.read_text
                def read(path, *args, **kwargs):
                    if str(path) == "/usr/share/aero7/base-packages.txt":
                        return "base\nlinux\n"
                    return original_read(path, *args, **kwargs)
                stack.enter_context(patch.object(Path, "read_text", read))
                with self.assertRaises(ReachedPackageInstall):
                    backend.install({"device": "/dev/vda", "layout": backend.SUPPORTED_LAYOUT,
                                     "keyboard": "Dutch", "language": "Nederlands"}, "/dev/vda")


if __name__ == "__main__":
    unittest.main()
