# Project boundaries

Aero7's installer image and desktop shell are separate projects.

## Aero7 ISO

The `aero7-open-project/aero7` repository owns the Archiso profile, graphical installer,
disk backend, OOBE, recovery environment, media validation, and ISO-specific
documentation. It does not own or vendor the Aero7-shell source repository.

## Aero7-shell

The `memegeko/aero7-shell` repository owns desktop configuration, staged
installation logic, recovery commands, application recipes, tests, and the
post-install integration used on an existing Arch system.

## Integration contract

`sources.lock` pins one reviewed shell origin and commit. The ISO build requires
the separate sibling clone to be clean and at that exact commit. It copies only
the runtime directories and entry points listed in `scripts/build-iso.sh` into
the temporary image profile. It never copies `.git`, tests, caches, release
documentation, or arbitrary repository contents, and it never writes into the
shell checkout.

This gives installed media a reproducible shell payload without merging the two
projects. Shell changes are tested and committed in Aero7-shell first; the ISO
pin is updated only after those checks pass.

## Beta 2 release boundary

Beta 2 source, package recipes, documentation and CI checks are published in
the project repository. The online ISO, offline ISO and checksums are separate
website release artifacts and are never attached to GitHub Releases. Exact
website-hosted bytes must match the accepted release hashes before their
download buttons are enabled.
