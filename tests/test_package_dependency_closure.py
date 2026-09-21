#!/usr/bin/env python3
"""Validate that the embedded Beta 2 transaction is dependency-complete."""

from __future__ import annotations

import hashlib
from pathlib import Path
import re
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


def dependency_name(value: str) -> str:
    return re.split(r"[<>=]", value, maxsplit=1)[0]


def read_list(path: Path) -> list[str]:
    return [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def manifest_packages(path: Path) -> list[Path]:
    packages: list[Path] = []
    for line in read_list(path):
        fields = line.split(maxsplit=1)
        if len(fields) != 2:
            raise AssertionError(f"invalid package manifest entry: {line}")
        packages.append(ROOT / fields[1])
    return packages


def package_metadata(path: Path) -> dict[str, list[str]]:
    text = subprocess.check_output(
        ["bsdtar", "-xOf", str(path), ".PKGINFO"],
        text=True,
        stderr=subprocess.DEVNULL,
    )
    metadata: dict[str, list[str]] = {}
    for line in text.splitlines():
        if " = " not in line:
            continue
        key, value = line.split(" = ", maxsplit=1)
        metadata.setdefault(key, []).append(value)
    return metadata


def capabilities(metadata: dict[str, list[str]]) -> set[str]:
    return {metadata["pkgname"][0]} | {
        dependency_name(value) for value in metadata.get("provides", [])
    }


def satisfies(dependency: str, metadata: dict[str, list[str]]) -> bool:
    match = re.fullmatch(r"([^<>=]+)(>=|<=|=|>|<)?([^<>=]*)", dependency)
    if not match:
        raise ValueError(f"invalid dependency: {dependency}")
    name, operator, expected = match.groups()
    offers = [metadata["pkgname"][0] + "=" + metadata["pkgver"][0]]
    offers += metadata.get("provides", [])
    for offer in offers:
        offered_name, _, version = offer.partition("=")
        if offered_name != name:
            continue
        if not operator:
            return True
        if not version:
            continue
        comparison = int(subprocess.check_output(["vercmp", version, expected], text=True))
        if {"=": comparison == 0, ">=": comparison >= 0, "<=": comparison <= 0,
            ">": comparison > 0, "<": comparison < 0}[operator]:
            return True
    return False


class DependencyVersionTests(unittest.TestCase):
    def test_old_version_does_not_satisfy_vault_requirement(self) -> None:
        old = {"pkgname": ["kwallet"], "pkgver": ["6.28.0-1"]}
        current = {"pkgname": ["kwallet"], "pkgver": ["6.29.0-1"]}
        self.assertFalse(satisfies("kwallet>=6.29.0", old))
        self.assertTrue(satisfies("kwallet>=6.29.0", current))

    def test_unversioned_provider_is_not_a_versioned_dependency(self) -> None:
        provider = {"pkgname": ["replacement"], "pkgver": ["99-1"], "provides": ["library"]}
        self.assertTrue(satisfies("library", provider))
        self.assertFalse(satisfies("library>=1", provider))
        provider["provides"] = ["library=2"]
        self.assertTrue(satisfies("library>=1", provider))
        self.assertFalse(satisfies("library=1", provider))

    def test_epoch_and_package_release_use_pacman_comparison(self) -> None:
        package = {"pkgname": ["example"], "pkgver": ["1:6.7.4-3"]}
        self.assertTrue(satisfies("example>6.7.4-99", package))
        self.assertTrue(satisfies("example=1:6.7.4", package))
        self.assertFalse(satisfies("example>=1:6.7.4-4", package))


class PackageDependencyClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        bundle_manifests = (
            ROOT / "config/offline-base-packages.sha256",
            ROOT / "config/offline-aero7-packages.sha256",
        )
        missing_bundle_files = [
            path
            for manifest in bundle_manifests
            for path in manifest_packages(manifest)
            if not path.is_file()
        ]
        if missing_bundle_files:
            raise unittest.SkipTest(
                "generated offline package bundle is not present; "
                "run scripts/prepare-offline-packages.sh before validating its closure"
            )

        cls.base = [
            (path, package_metadata(path))
            for path in manifest_packages(ROOT / "config/offline-base-packages.sha256")
        ]
        cls.aero7 = [
            (path, package_metadata(path))
            for path in manifest_packages(ROOT / "config/offline-aero7-packages.sha256")
        ]
        cls.local = [
            (path, package_metadata(path))
            for path in manifest_packages(ROOT / "config/beta2-local-packages.sha256")
        ]

    def test_firewalld_offline_recursive_versioned_dependencies(self) -> None:
        # The earlier local-transaction check only verifies dependencies of
        # Aero7 packages. The new fresh-install firewall lives in the base
        # bundle and needs its complete Python/library chain, including SONAME
        # and exact-version requirements, without using network resolution.
        providers = {}
        for path, metadata in self.base:
            entries = [metadata["pkgname"][0] + "=" + metadata["pkgver"][0]]
            entries += metadata.get("provides", [])
            for entry in entries:
                name, _, version = entry.partition("=")
                providers.setdefault(name, []).append((version, path, metadata))
        self.assertNotIn("ufw", providers,
                         "Offline pacstrap installs every base archive; UFW must not be in the fresh-install bundle")
        pending = ["firewalld"]
        visited = set()
        while pending:
            dependency = pending.pop()
            match = re.fullmatch(r"([^<>=]+)([<>=]+)?(.*)", dependency)
            self.assertIsNotNone(match, dependency)
            name, operator, expected = match.groups()
            selected = None
            for version, path, metadata in providers.get(name, []):
                if operator:
                    if not version:
                        continue
                    comparison = int(subprocess.check_output(["vercmp", version, expected], text=True))
                    if not {"=": comparison == 0, ">=": comparison >= 0,
                            "<=": comparison <= 0, ">": comparison > 0,
                            "<": comparison < 0}.get(operator, False):
                        continue
                selected = (path, metadata)
                break
            self.assertIsNotNone(selected, "Missing offline firewall dependency: " + dependency)
            path, metadata = selected
            if path in visited:
                continue
            visited.add(path)
            pending.extend(metadata.get("depend", []))

    def test_local_transaction_dependencies_are_satisfied(self) -> None:
        base_capabilities = set().union(
            *(capabilities(metadata) for _, metadata in self.base)
        )
        required_local_names = set(read_list(ROOT / "config/beta2-local-package-names.txt"))
        optional_local_names = set(read_list(ROOT / "config/beta2-optional-package-names.txt"))
        manifest_local_names = {metadata["pkgname"][0] for _, metadata in self.local}
        self.assertEqual(
            manifest_local_names,
            required_local_names | optional_local_names,
            "every embedded package must be declared required or optional",
        )
        self.assertFalse(
            required_local_names & optional_local_names,
            "an embedded package cannot be both required and optional",
        )
        required_local = [
            item for item in self.local if item[1]["pkgname"][0] in required_local_names
        ]
        optional_local = [
            item for item in self.local if item[1]["pkgname"][0] in optional_local_names
        ]
        required_local_capabilities = set().union(
            *(capabilities(metadata) for _, metadata in required_local)
        )
        providers: dict[str, list[tuple[Path, dict[str, list[str]]]]] = {}
        for path, metadata in self.aero7:
            for capability in capabilities(metadata):
                providers.setdefault(capability, []).append((path, metadata))

        requested = read_list(ROOT / "config/aero7-packages.txt")
        embedded = required_local_names
        queue = [package for package in requested if package not in embedded]
        selected: dict[str, tuple[Path, dict[str, list[str]]]] = {}
        unresolved: list[str] = []
        while queue:
            dependency = queue.pop(0)
            name = dependency_name(dependency)
            if name in base_capabilities or name in required_local_capabilities or name in selected:
                continue
            choices = providers.get(name, [])
            if not choices:
                unresolved.append(dependency)
                continue
            choices.sort(
                key=lambda item: (
                    item[1]["pkgname"][0] == name,
                    item[0].name,
                )
            )
            chosen = choices[-1]
            for capability in capabilities(chosen[1]):
                selected[capability] = chosen
            queue.extend(chosen[1].get("depend", []))

        self.assertEqual([], unresolved, "repository package transaction is incomplete")
        installed = base_capabilities | required_local_capabilities | set(selected)
        missing: dict[str, list[str]] = {}
        for _, metadata in required_local:
            package_missing = [
                dependency
                for dependency in metadata.get("depend", [])
                if dependency_name(dependency) not in installed
            ]
            if package_missing:
                missing[metadata["pkgname"][0]] = package_missing
        self.assertEqual({}, missing, "embedded package transaction has missing dependencies")

        optional_capabilities = set().union(
            *(capabilities(metadata) for _, metadata in optional_local)
        )
        optional_available = installed | optional_capabilities
        optional_missing: dict[str, list[str]] = {}
        for _, metadata in optional_local:
            missing_dependencies = [
                dependency
                for dependency in metadata.get("depend", [])
                if dependency_name(dependency) not in optional_available
            ]
            if missing_dependencies:
                optional_missing[metadata["pkgname"][0]] = missing_dependencies
        self.assertEqual(
            {}, optional_missing,
            "locally retained optional packages have missing dependencies",
        )

        # Check versions against the final selected set, not an obsolete base
        # archive that a local replacement removes. This is a metadata check,
        # not a substitute for a real pacman transaction or boot test.
        replacements = {metadata["pkgname"][0]: metadata
                        for _, metadata in list(selected.values()) + required_local}
        final = {metadata["pkgname"][0]: metadata for _, metadata in self.base
                 if metadata["pkgname"][0] not in replacements
                 and not any(satisfies(conflict, metadata)
                             for replacement in replacements.values()
                             for conflict in replacement.get("conflict", []))}
        final.update(replacements)
        conflicts = [(name, other, conflict)
                     for name, metadata in final.items()
                     for conflict in metadata.get("conflict", [])
                     for other, provider in final.items()
                     if other != name and satisfies(conflict, provider)]
        self.assertEqual([], conflicts, "final package set contains mutually conflicting packages")
        versioned_missing = {}
        for name, metadata in final.items():
            absent = [dependency for dependency in metadata.get("depend", [])
                      if not any(satisfies(dependency, provider) for provider in final.values())]
            if absent:
                versioned_missing[name] = absent
        self.assertEqual({}, versioned_missing, "final package set has unsatisfied versioned dependencies")
        for _, metadata in optional_local:
            available = list(final.values()) + [metadata]
            absent = [dependency for dependency in metadata.get("depend", [])
                      if not any(satisfies(dependency, provider) for provider in available)]
            self.assertEqual([], absent, metadata["pkgname"][0]
                             + " cannot be enabled independently from the offline cache")

    def test_older_embedded_kwallet_is_rejected(self) -> None:
        # Mutate only in-memory metadata; archives and host packages stay intact.
        self.base = [(path, {**metadata, "pkgver": ["6.28.0-1"]}
                      if metadata["pkgname"][0] == "kwallet" else metadata)
                     for path, metadata in self.base]
        with self.assertRaisesRegex(AssertionError, r"kwallet>=6\.29\.0"):
            self.test_local_transaction_dependencies_are_satisfied()

    def test_one_optional_feature_cannot_supply_anothers_dependency(self) -> None:
        self.local = [(path, {**metadata, "depend": metadata.get("depend", [])
                              + ["aero7-credential-vault"]}
                       if metadata["pkgname"][0] == "aero7-programs-center-git" else metadata)
                      for path, metadata in self.local]
        with self.assertRaisesRegex(AssertionError, "cannot be enabled independently"):
            self.test_local_transaction_dependencies_are_satisfied()

    def test_internet_explorer_uses_approved_icon_pack_asset(self) -> None:
        package = next(
            path
            for path, metadata in self.local
            if metadata["pkgname"][0] == "aero7-internet-explorer"
        )
        icon = subprocess.check_output(
            [
                "bsdtar",
                "-xOf",
                str(package),
                "usr/share/icons/hicolor/256x256/apps/aero7-internet-explorer.png",
            ]
        )
        self.assertEqual(
            "b3fd991c7718a876e06f3ae42e9b5a0eb25cf5876ad01d581fdff99851e4f98e",
            hashlib.sha256(icon).hexdigest(),
        )


if __name__ == "__main__":
    unittest.main()
