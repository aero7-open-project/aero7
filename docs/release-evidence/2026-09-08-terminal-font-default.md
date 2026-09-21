# Terminal fixed-pitch default — 8 September 2026

Local component QA; no release or publication approval.

## Cause and correction

The installed QTerminal/QTermWidget 2.4.0 generic `Monospace` request resolves
to Noto Sans Mono, whose Qt font information reports `fixedPitch=false` here.
ASCII advances measured equal, so this is not evidence of existing ASCII
alignment damage. It nevertheless triggers the terminal's diagnostic.
[QTermWidget initializes a generic font before application preferences](https://github.com/lxqt/qtermwidget/blob/2.4.0/lib/qtermwidget.cpp),
which explains why the earlier explicit QTerminal preference left one warning.
[The diagnostic checks Qt's fixed-pitch flag](https://github.com/lxqt/qtermwidget/blob/2.4.0/lib/TerminalDisplay.cpp).

Desktop 30 supplies `/etc/fonts/conf.d/60-aero7-monospace.conf`, preferring the
existing DejaVu Sans Mono font only for generic monospace requests. It declares
fontconfig and ttf-dejavu dependencies. It changes no font files, icon artwork,
QTerminal binary, explicit application font settings or user's configuration.
This is a system-wide generic monospace default, also applicable to editors;
the sans-serif and serif defaults remain unchanged.

The rule is ordered after per-user configuration and before the standard
generic aliases. The initial 49-prefix proposal failed the custom-user-alias
test and was corrected to 60 before packaging. Fontconfig's
[configuration ordering](https://fontconfig.pages.freedesktop.org/fontconfig/fontconfig-user.html)
is tested using isolated copies of the actual system include layout.

## Evidence and test-fixture correction

- Baseline VM QTerminal emitted three warnings with the default profile, one
  with an explicit DejaVu profile, and one with a custom Liberation profile.
- The earlier hand-written legacy fixture was invalid: its unquoted comma
  list did not represent a QFont value. The first run stopped at that assertion.
  The revised fixture is serialized by QSettings with a real QFont. Its normal
  conversion to `fontFamily=Liberation Mono` and `fontSize=14` passes.
- The process-local comparison has zero warnings for all four candidate
  profiles. The real user's QTerminal file hash is unchanged. Qt measurements
  show fixed-pitch generic selection and equal ASCII advances at 10, 12, 14
  and 24 points. An explicit Noto Sans Mono request still resolves to Noto;
  its metadata warning is not hidden or suppressed.
- Four real-fontconfig tests pass: generic selection including bold,
  explicit-family preservation, unchanged UI families and user-alias priority.
- All eight Desktop source CTest suites pass (15.32 seconds), including staged
  production, test-image and developer installs. The package's eight suites
  also pass (15.92 seconds).

Comparison evidence: `terminal-font-logs/font-fallback.iKS39k/` retains the
failed fixture run; `font-fallback.W09D34/` retains the corrected comparison.
The package build log is retained alongside them. No warnings were filtered
from these captured logs.

## Package identity

Local build directory: `work/beta2-desktop30.BA2ezA/`.
Built with `makepkg --nodeps` to avoid changing the host package set; this is
not clean-builder or signed-repository acceptance.

- Source archive: `aero7-desktop-0.2.0-r30.tar.gz`
- Source SHA-256: `09fa28a4c643056434c98bccbca61537792b1ab18ced6ace918f24fb1f6a3545`
- Package: `aero7-desktop-0.2.0-30-x86_64.pkg.tar.zst`
- Size: 1,986,111 bytes
- Package SHA-256: `1ddbc04b3640d18b78217a9d58317f677f1fef98835449c7748d7cfb9b369746`
- Rule SHA-256: `69aa7b25d0243dab4410088637f790de016c2b3a4bbb7d140c3898932768fcbb`

The package path inventory adds only the fontconfig rule and its parent
directories. No previous payload path was removed. The standalone source
recipe and the local QA recipe both declare the two font dependencies.

## Acceptance boundary

The normal disconnected upgrade changed only Desktop 29 to 30. All 78 package
files were present, the rule hash matched, and the user's QTerminal file stayed
byte-identical. All four installed profile cases passed without environment
fontconfig/library overrides; custom and valid legacy Liberation settings were
preserved. A normal taskbar terminal launch (PID 5870 at 17:00:26) also passed:
no variable-width warning in its journal, no fontconfig/library overrides in its
environment, and the user's existing `Monospace`, 12-point preference resolved
to the fixed-pitch fallback. Shell and firewalld remained active.

The first upgrade command was intercepted by the five-minute idle lock before
the helper ran. Its authentication error and successful normal unlock are QA
input events, not package failure. The actual transaction started at 16:58:01.

Normal reboot/password login subsequently passed. The 17:03:33 audit checked a
new boot ID, the installed package and exact rule hash, all 78 files, a fresh
normal taskbar QTerminal process without environment overrides, and fixed-pitch
font metrics. No terminal-font warning appears in the new process journal or
the retained full user journal. Shell, screenshot helper, update-check timer
and firewalld were active; failed-unit snapshots were empty. This is not a
clean-journal claim: portal registration and disabled-wallet activation errors
remain in `desktop30-reboot-user-journal.log`.

Final online/offline media acceptance remains required. The frozen r10 images
still contain Desktop 29, not this correction. Existing portal/credential-store
issues and early-Escape screenshot timing remain separate open issues.
Nothing was committed, pushed, signed or published.
