# Theme 45 — package-owned login and lock-screen corrections

Local package/source work. Normal guest upgrade and restart checks passed below;
final fresh-media acceptance remains pending.
No package was committed, signed, promoted or published by this pass.

## Ownership correction

Theme 45 includes the existing approved Welcome JPEG in its three already-owned
SDDM files: `background`, `default-background` and `preview.png`. It also packages
the precise white `btnLabel` correction previously applied by the installer.
The existing approved logo, AuthUI sizing and `Image.PreserveAspectFit` remain
unchanged. No new icons, logos or artwork were created.

The package deliberately does not own `bgtexture.jpg`: the pinned Shell creates
that file outside package ownership, and adopting it would conflict during an
ordinary upgrade. The current Main.qml does not use it. The immutable pinned
Shell tree remains unchanged; its unconditional background copies can still
change modification times during a full explicit Shell reapplication.

The installer now recognizes precisely branded label blocks with blank lines
before or after the white color. It still rejects the wrong label or color.
Accepted prebranded files retain both bytes and modification times. The new
regression failed before this correction; all 135 backend tests now pass.

## Build and archive evidence

- Package: `aerothemeplasma-desktop-git-6.7.0_742.r9c2d850-45-x86_64.pkg.tar.zst`.
- Size: 5,139,658 bytes.
- SHA-256: `b320f28842773553dd00ec3d2a11a10b5c74ad5e7c8f14166f5dada1539c469e`.
- PKGBUILD SHA-256: `bac87cf88c6516fdd95bd5ad34a8d37855505f3c6b937f039715ba75c6b18bb7`.
- SRCINFO SHA-256: `4ef9ad710f40c2d8de6d62721fd31357203175f9f377ba0bae0c7d4206e2af0f`.
- Welcome JPEG SHA-256: `65e825c2dcc1b0c80d14896a6108199d825f8dc7b44724f22fe19d8b308fb7e7`.
- Approved logo SHA-256: `d45164d6d67f2d8ccae63c4fd83bd0dd73e05808f3c8cd739c4850b5680d4982`.
- Label patch SHA-256: `cbfd0340c8a7103b822d379e86ca7ab52e5b6f75372f4d637f0ee7a544cb104f`.

The two-job build finished on 7 September at 00:54:48 CEST under
`work/beta2-theme45.OdUiCT`; all 15 CTest groups passed in 0.63 seconds.
An initial build was interrupted after identifying the prospective bgtexture
ownership conflict. Only package staging changed; the verified prepared source
was reused with `--noextract`, and build/check/package ran successfully. No tests
were skipped. The upstream commit remains pinned and no host packages changed.

`scripts/verify-theme-branding.py` rejects the old package 44 background and
accepts package 45. It verifies exact artwork hashes and references, then runs
lock-screen setup twice against actual extracted package files and checks that
neither bytes nor timestamps change. The ISO static checker now includes this
gate. This archive evidence does not establish live rendering or update survival.

Theme 45 and Explorer 43 are selected in the next-ISO input manifest. The
immutable r9 online/offline images still contain older versions; final media
must be rebuilt and tested separately.

## Normal installed upgrade and reboot

The disconnected r9 guest upgraded normally from theme 44 to 45 with dependency
resolution enabled, no forced overwrite and no other package changes. Its 1,143
theme files, 665 Explorer files and 709 Paint files all reported zero alterations.
Paint preferences retained their checksum. A normal system restart returned to
SDDM and password login reached the desktop. Different exported boot IDs prove
the new boot; the repeated package audit still reports zero altered files.

1920×1080 evidence under `/home/admin/VMs/aero7-beta2-r9-xTfYQR/offline/`:

- 285: successful upgrade and integrity results.
- 287: post-reboot SDDM, complete Aero7 Professional logo and intended background.
- 288: successful desktop login.
- 292: actual locked session, complete logo and readable white Switch User label.
- 293: successful password unlock back to the existing desktop session.

The QA shares were manually remounted after reboot; an initial audit invocation
failed because they were not mounted. This is test-fixture setup, not a package
repair. An early typed command also reached the desktop runner before the
terminal was ready, producing an unsuccessful sudo launch; those warnings are
retained rather than attributed to the installer.

The system-unit audit lists zero failed units, but the journal is not clean.
It still records SDDM Column/layout conflicts and an undefined keyboard shortName,
KWallet/portal and service-name warnings, virtual-device warnings and a KSplash
user-service failure. These need separate classification/correction. SDDM stopped
in the same logged second as its stop request, but recorded helper exit errors;
this does not prove the older intermittent whole-session shutdown issue fixed.

No full Shell reapplication or fresh installation was performed in this check.
The pinned Shell's metadata behavior remains a separate gate. Logs are retained
in `theme-branding-logs/`, including before-upgrade integrity and current-boot
warnings. Passing branding/integrity checks are not warning-free desktop acceptance.

The additional user-session diagnostic identifies the splash failure more
precisely: `plasma_waitforname` waited from 01:11:34 to 01:12:34 for
`org.kde.KSplash`, then exited with status 1 because the service name never
registered. A later `systemctl show` of the vanished transient unit reported
default success fields; the journal, not those fields, is the failure evidence.
The only currently failed user unit was the QA-induced desktop-runner sudo
attempt described above. The previous user journal contained no matches for
the targeted stop-timeout/forced-kill patterns; this is not a universal shutdown
guarantee. No services were reset or disabled to clear these diagnostics.
