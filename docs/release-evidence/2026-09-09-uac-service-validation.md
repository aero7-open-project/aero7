# Authentication service and fallback validation — 9 September 2026

Status: the duplicate-service and disabled-selector defects are fixed in a local,
normally installed candidate. This is not final-image or complete desktop acceptance.

## Defects and correction

The installed original package supplied two separate units claiming
`org.kde.polkit-kde-authentication-agent-1`. Merely loading the unused
`uac-polkit-agent.service` reproduced systemd's duplicate-bus-name refusal;
the running `plasma-polkit-agent.service` remained active. This was a packaging
conflict, not evidence that earlier approved transactions lacked authentication.

The old selector also treated `USE_UAC_AGENT=0` as enabled, although the Aero
executable exits immediately for that value. The candidate matches the executable:
unset, empty and exactly `0` select the Plasma agent; other nonempty values select
Aero. Quoted shell handling also fixes values containing whitespace.

The old service name is now a relative symlink to the canonical Plasma unit,
following [systemd's unit alias mechanism](https://github.com/systemd/systemd/blob/main/man/systemd.unit.xml).
Both names address one supervised agent and retain `Type=dbus`, its original
bus name, graphical-session lifetime and restart policy. The package explicitly
depends on `polkit-kde-agent`, which owns the canonical unit and fallback binary.
No polkit rules, password requirements, dumpability or ptrace protections changed.
The upstream and candidate `main.cpp` are byte-identical, SHA-256
`ff72d430e0a4bbe65b9684a07eacc91dfeb3a4ac286f845cd9828f624947cc36`;
the build still sets `HAVE_PR_SET_DUMPABLE=1`.

## Candidate and build

- Upstream: `d8c2262f5a12fe1a53560e70414b9312b91d84bb`.
- Package: `uac-polkit-agent-git-6.7.0_816.rd8c2262-2-x86_64.pkg.tar.zst`.
- Size: 105,315 bytes.
- SHA-256: `38e9b7c690671c355a87fe7ce0c676719775706e183acd552167fe3813717132`.
- Patch SHA-256: `037023d5440c5359154a217718c1e2ce0da90842cca3726cdca5a65263b8620f`.
- Build: 01:13:30–01:13:51 CEST, two jobs. CTest reports two successful statuses,
  but ECM's metadata test says “Not installed yet, skipping”; it is not a passed
  metadata validation. The executed selector suite passes all seven
  inert-executable cases. Three fail on the old selector. This tests selection,
  not GUI authentication by itself.
- The archive contains the alias and executable launcher, not a second copy of
  the canonical unit. Package installation checked the alias target explicitly.

The [recipe](uac2-logs/PKGBUILD), [patch](uac2-logs/aero7-single-agent.patch),
[full build log](uac2-logs/uac2-package.log),
[CTest details](uac2-logs/package-LastTest.log) and
[old-selector failures](uac2-logs/baseline-selection.log) are retained.
The build used existing host dependencies, with makepkg dependency checks skipped;
the guest upgrade used normal dependency/conflict checking. No host packages were installed.

## Installed VM evidence

The 1920×1080 Wayland online guest upgraded normally from package release 1 to 2;
no other package changed. All 222 UAC package files and 217 fallback package files
were present. A normal reboot and password login passed.

- [Original conflict](uac2-logs/uac-baseline.HX8kky/audit.log).
- [Normal upgrade](uac2-logs/uac2-upgrade.rKb0Wz/upgrade.log).
- [First reboot audit](uac2-logs/uac2-audit.YoSVGl/audit.log), boot
  `57cc7601-30f9-416a-bf7a-6ab47f03f121`.
- [Resumed cold-boot audit](uac2-logs/uac2-audit.7k9yK7/audit.log), boot
  `1d831b02-7883-4b6a-ba90-f24f6c0d407d`.

Both service names resolve to the same active PID and canonical unit. Starting
the alias while active does not restart the process. Neither cold-boot journal
contains the duplicate-bus-name refusal; shell and authentication units have
zero automatic restarts, and failed-unit lists were empty at the audit snapshots.

The [completed interactive replay](uac2-logs/uac2-prompts.edOD0M/prompts.log)
uses `pkexec --disable-internal-agent /usr/bin/id -u`: a harmless identity query
that cannot use a terminal authentication fallback. Four real dialogs were observed:

| Agent | GUI action | Observed result |
| --- | --- | --- |
| Aero | Enter administrator password | Exit 0, root UID `0` returned |
| Aero | Cancel | Exit 127, Not authorized, no UID output |
| Plasma with `USE_UAC_AGENT=0` | Enter administrator password | Exit 0, root UID `0` returned |
| Plasma | Cancel | Exit 127, Not authorized, no UID output |

The test restored `USE_UAC_AGENT=1` and the Aero agent afterwards. Package inventory
and the core polkit action policy checksum are unchanged across the replay.
Both agents report dismissal as Not authorized (127), rather than the distinct
126 status described by pkexec; that behavior is recorded, not relabeled or fixed
by this patch. An initial test stopped on its overly specific 126 assertion, and
a second attempt was interrupted when the VM stopped; neither counts as a pass.
Their original logs remain beside the completed replay.

Screenshots: [Aero approval](uac2-logs/294-aero-approve-replay.png),
[Aero cancellation](uac2-logs/295-aero-cancel-replay.png),
[Plasma approval](uac2-logs/296-plasma-approve.png),
[Plasma cancellation](uac2-logs/297-plasma-cancel.png).

## Boundaries and remaining work

The protected-process `/proc/PID/root` portal diagnostic occurs for both real
agents and remains; their authentication succeeds without weakening protection.
The complete replay journal also retains the existing Aero shortcut/image-reply
diagnostics. No claim of an entirely warning-free authentication UI is made.
KWallet/default secret-store policy and the misleading Credential Manager route
remain separate issues. Broader workflow, recovery and hardware checks continue.

The package is a local QA candidate only. Repository promotion, final-image
integration, final online/offline acceptance and website publication remain held.
No commits, pushes, repository uploads or final ISO builds were performed.
