#!/usr/bin/env python3
"""Check candidate package hygiene and offline repository/manifest agreement.

Archives are streamed, never extracted. Only the checksum-selected candidate
and Aero7 dependency archives are in scope, not old developer cache files.
"""
from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import tarfile
from pathlib import Path, PurePosixPath


def forbidden_member(name: str) -> bool:
    path = PurePosixPath(name)
    return path.is_absolute() or bool(set(path.parts) & {"..", ".git", ".svn", ".hg", ".bzr"})


def manifest(root: Path, filename: str) -> dict[Path, str]:
    result = {}
    for line in (root / filename).read_text().splitlines():
        digest, relative = line.split(None, 1)
        path = PurePosixPath(relative)
        if path.is_absolute() or ".." in path.parts or len(digest) != 64:
            raise ValueError(f"Invalid manifest entry in {filename}")
        if root / relative in result:
            raise ValueError(f"Duplicate manifest entry: {relative}")
        result[root / relative] = digest
    return result


def inspect_archive(path: Path, expected: str) -> dict[str, str]:
    with path.open("rb") as stream:
        if hashlib.file_digest(stream, "sha256").hexdigest() != expected:
            raise ValueError(f"Checksum mismatch: {path.name}")
    metadata = {}
    forbidden = []
    with subprocess.Popen(["zstd", "-dc", "--", str(path)], stdout=subprocess.PIPE) as process:
        with tarfile.open(fileobj=process.stdout, mode="r|") as archive:
            for member in archive:
                if forbidden_member(member.name):
                    forbidden.append(member.name)
                if member.name == ".PKGINFO" and member.isfile():
                    for line in archive.extractfile(member).read().decode().splitlines():
                        if " = " in line:
                            key, value = line.split(" = ", 1)
                            if key in {"pkgname", "pkgver"}:
                                metadata[key] = value
        if process.wait() != 0:
            raise ValueError(f"Decompression failed: {path.name}")
    if forbidden:
        raise ValueError(f"{path.name}: {len(forbidden)} forbidden archive paths, including {forbidden[0]}")
    if set(metadata) != {"pkgname", "pkgver"}:
        raise ValueError(f"Missing package identity: {path.name}")
    return metadata


def repository_entries(path: Path) -> dict[str, dict[str, str]]:
    result = {}
    with tarfile.open(path, "r:gz") as archive:
        for member in archive:
            if not member.isfile() or not member.name.endswith("/desc"):
                continue
            fields = {}
            for block in archive.extractfile(member).read().decode().strip().split("\n\n"):
                key, _, value = block.partition("\n")
                fields[key.strip("%")] = value.strip()
            filename = fields["FILENAME"]
            if filename in result:
                raise ValueError(f"Duplicate offline repository entry: {filename}")
            result[filename] = fields
    return result


def verify_release_notes(notes: str, identities: list[dict[str, str]], optional: set[str]) -> None:
    heading = "## Current local candidate packages\n"
    if heading not in notes:
        raise ValueError("Release notes are missing the current candidate package table")
    section = notes.split(heading, 1)[1].split("\n## ", 1)[0]
    expected = {entry["pkgname"]: entry["pkgver"] for entry in identities}
    if len(expected) != len(identities):
        raise ValueError("Duplicate selected package identity")
    rows = re.findall(r"^\| `([^`]+)`( \(optional\))? \| `([^`]+)` \|$", section, re.M)
    actual = {}
    marked_optional = set()
    for name, marker, version in rows:
        if name in actual:
            raise ValueError(f"Duplicate release-notes package: {name}")
        actual[name] = version
        if marker:
            marked_optional.add(name)
    if actual != expected:
        raise ValueError("Release-notes package versions differ from selected archive metadata")
    if marked_optional != optional:
        raise ValueError("Release-notes optional package labels differ from package policy")


def verify_distinct_package_sources(local: list[dict[str, str]], offline: list[dict[str, str]]) -> None:
    local_names = {entry["pkgname"] for entry in local}
    offline_names = {entry["pkgname"] for entry in offline}
    overlap = sorted(local_names & offline_names)
    if overlap:
        raise ValueError(
            "Offline repository duplicates checksum-pinned local packages: "
            + ", ".join(overlap)
        )


def verify(root: Path, variant: str) -> None:
    local = manifest(root, "config/beta2-local-packages.sha256")
    offline = manifest(root, "config/offline-aero7-packages.sha256") if variant == "offline" else {}
    identities = {path: inspect_archive(path, digest) for path, digest in {**local, **offline}.items()}
    optional = {line.strip() for line in (root / "config/beta2-optional-package-names.txt").read_text().splitlines()
                if line.strip() and not line.lstrip().startswith("#")}
    verify_release_notes((root / "docs/BETA2-RELEASE-NOTES.md").read_text(),
                         [identities[path] for path in local], optional)
    if offline:
        verify_distinct_package_sources(
            [identities[path] for path in local],
            [identities[path] for path in offline],
        )
        repo = root / "offline-packages/aero7-offline.db.tar.gz"
        repo_manifest = manifest(root, "config/offline-aero7-repo.sha256")
        with repo.open("rb") as stream:
            if hashlib.file_digest(stream, "sha256").hexdigest() != repo_manifest[repo]:
                raise ValueError("Offline repository checksum mismatch")
        entries = repository_entries(repo)
        if set(entries) != {path.name for path in offline}:
            raise ValueError("Offline repository file list differs from the package manifest")
        for path, digest in offline.items():
            entry, identity = entries[path.name], identities[path]
            if (entry["SHA256SUM"], entry["NAME"], entry["VERSION"]) != (digest, identity["pkgname"], identity["pkgver"]):
                raise ValueError(f"Offline repository identity/checksum mismatch: {path.name}")
    print(f"PASS {len(identities)} {variant} candidate/custom dependency archives: no VCS metadata or unsafe paths")
    print(f"PASS release notes match {len(local)} selected package versions and optional-package policy")
    if offline:
        print(f"PASS {len(offline)} offline repository entries match package identities and checksums")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", choices=("online", "offline"), required=True)
    parser.add_argument("--project-root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        verify(args.project_root.resolve(), args.variant)
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        parser.exit(1, f"Candidate package verification failed: {error}\n")
