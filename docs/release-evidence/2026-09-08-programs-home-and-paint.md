# Programs Center Home layout and Paint launcher identity

Component verification, 8 September 2026. **Not release approval.** These
changes are installed in the r10 offline test guest only. The frozen r10
ISOs still contain Programs Center package release 2 and Paint release 8.

## Corrections

Programs Center's fixed-column Home grids overflowed the available central
pane. Featured programs, recommended programs and category links now use an
equal-width wrapping layout. Rows adapt to the available viewport, including
when shrinking after a wider layout. Card text remains word-wrapped and
vertical scrolling remains available. Existing package actions are unchanged.

The stale “KolourPaint” label came from the installed
`/usr/share/applications/org.kde.kolourpaint.desktop`, not a Programs Center
override. Paint packaging now supplies `Name=Paint`, including localized
application-name keys. The desktop ID, `Exec=kolourpaint %u`, icon, MIME types
and other fields are preserved. Comparing the release 8 and 9 archives found
no other changed payload files: only this desktop file and package metadata
(`.BUILDINFO`, `.PKGINFO`, `.MTREE`) differed. The compiled program was reused
for this packaging-only change; this was not a new Paint source build.

## Exact candidate packages

| Package | SHA-256 |
| --- | --- |
| `aero7-programs-center-git-0.1.0.r12.g0405a2e-3-x86_64.pkg.tar.zst` | `0b84b21b0e82f92900c5711034f09386ab04a7ea1acc2f617420a5b673880946` |
| `aero7-kolourpaint-25.12.3-9-x86_64.pkg.tar.zst` | `fc52b3524e9629f92176217e5bfaa5365d152798f84a624ff4a356a8236bb812` |

Programs Center was built from pinned upstream commit
`0405a2ef42c96d253a9436b3413fdccfe7c1cb09` with the combined downstream
offline-inventory/layout patch, SHA-256
`cedbb4f4e0d48bec36aad8d0bce5fe9f1875c77123fdebc75c9e66f42a33a867`.
The patch applied cleanly. Both recipe `.SRCINFO` files match generated
metadata. No repository manifest or frozen ISO profile was promoted.

## Test evidence

- All five CTest suites passed in both the source build and the final package
  build: core, offline backend, icon independence, Home layout and icon policy.
- The new layout regression uses the real MainWindow with eight long-title,
  long-description cards. It checks 1600 → 1200 → 900 → 1200 pixel widths,
  content/viewport bounds, card intersections, wrapped label bounds, and
  empty/single-card layouts. Test settings use a temporary directory.
- The initial fixed-delay test failed under the actual Wayland compositor.
  Geometry logging demonstrated that a requested resize could still report
  the previous window size after 100 ms. The test now waits for the requested
  size and settled viewport width. The original failure is retained in
  `r10-logs/offline-layout-initial.log`; it is not counted as a pass.
- Three consecutive final Wayland replays passed, four Qt test results each
  including setup/cleanup. These ran in the installed desktop session, not
  with an offscreen platform override.
- A normal authenticated `pacman -U` upgraded the two exact local packages.
  The guest remained disconnected with only loopback networking. Before/after
  complete package lists differ only in these two version numbers. Queries
  retained expected missing-repository-database warnings; no refresh ran.
- Programs Center has 49 package files and Paint 709, with zero missing files.
  No failed system units were listed after the upgrade.
- The installed application launched normally. At the usual window width it
  shows two recommended-card columns; manual narrowing reflows to one and
  wraps category links without Home-page horizontal overflow. Search displays
  **Paint**, version `25.12.3-9`, with its existing icon and Installed status.

Evidence is copied to `r10-logs/offline-layout-paint-components.log` and the
before/after package lists alongside it. Screenshots are original 1920×1080
guest captures:

- `r10-logs/offline-programs-home-wide.png`
- `r10-logs/offline-programs-home-narrow.png`
- `r10-logs/offline-programs-paint-name.png`

The package build retains an existing AutoMoc warning for the old core test's
macro formatting; the build is not described as warning-free. The narrow
search-results table still has its own horizontal scrollbar; this correction
targets Home grids and does not claim responsive behavior for every page.

## Remaining gates

Final image selection/rebuild and fresh-media regression are still required.
Programs Center remains optional and Beta. Authentication cancellation,
invalid-bundle recovery, retained user data, broader package transactions and
the remaining desktop acceptance matrix are not certified by these checks.
The prior r10 optional-feature install/remove/reinstall evidence remains valid
for its original package release 2, not automatically for this new release 3.
No GitHub commit, push, publication, host package change or firewall change
was performed for this component pass.
