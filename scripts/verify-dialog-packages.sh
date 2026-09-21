#!/usr/bin/env bash
# Verify the native Paint/Explorer dialog dependency before composing an ISO.
set -Eeuo pipefail
explorer=$(realpath -e "${1:?File Explorer package}")
paint=$(realpath -e "${2:?Paint package}")
explorer_info=$(bsdtar -xOf "$explorer" .PKGINFO)
paint_info=$(bsdtar -xOf "$paint" .PKGINFO)
grep -Fqx 'pkgname = aero7-file-explorer' <<<"$explorer_info"
grep -Fqx 'pkgname = aero7-kolourpaint' <<<"$paint_info"
if ! grep -Fqx 'depend = aero7-file-explorer>=25.12.3-36' <<<"$paint_info"; then
    printf 'Paint must require the Explorer package that supplies its native dialog library.\n' >&2
    exit 1
fi
entries=$(bsdtar -tf "$explorer")
for entry in usr/lib/libaero7commondialogs.so.1 \
             usr/lib/libaero7commondialogs.so.1.0.0 \
             usr/lib/cmake/Aero7CommonDialogs/Aero7CommonDialogsConfig.cmake \
             usr/include/Aero7CommonDialogs/aero7commondialog.h; do
    if ! grep -Fqx "$entry" <<<"$entries"; then
        printf 'Explorer is missing a common-dialog runtime/SDK file: %s\n' "$entry" >&2
        exit 1
    fi
done
inspection_dir=$(mktemp -d "${TMPDIR:-/tmp}/aero7-dialog-packages.XXXXXX")
trap 'rm -f -- "$inspection_dir/paint" "$inspection_dir/dialog" "$inspection_dir/library"; rmdir -- "$inspection_dir"' EXIT
bsdtar -xOf "$paint" usr/bin/kolourpaint > "$inspection_dir/paint"
bsdtar -xOf "$explorer" usr/bin/aero7-file-dialog > "$inspection_dir/dialog"
bsdtar -xOf "$explorer" usr/lib/libaero7commondialogs.so.1.0.0 > "$inspection_dir/library"
for consumer in paint dialog; do
    dynamic=$(LC_ALL=C readelf -d "$inspection_dir/$consumer")
    grep -Fq 'Shared library: [libaero7commondialogs.so.1]' <<<"$dynamic"
    if grep -Eq '\((RPATH|RUNPATH)\).*(/home/|/tmp/|/work/)' <<<"$dynamic"; then
        printf 'A dialog consumer retains a temporary build-library path: %s\n' "$consumer" >&2
        exit 1
    fi
done
dynamic=$(LC_ALL=C readelf -d "$inspection_dir/library")
grep -Fq 'Library soname: [libaero7commondialogs.so.1]' <<<"$dynamic"
printf 'NATIVE_DIALOG_PACKAGE_LINKAGE_VERIFIED\n'
