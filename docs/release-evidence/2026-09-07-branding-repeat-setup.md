# Lock-screen branding: repeat-setup correction and ownership audit

Local installer source correction; no final ISO or fresh-install acceptance.
The pinned Aero7 Shell tree is unchanged. No packages were published.

## Reproduced repeat-setup failure

`brand_plasma_lock_screen()` inserts white text into GenericButton's `btnLabel`
block. A later invocation expected only the original block and rejected the
already-corrected block as an unexpected layout change. The new regression
demonstrated that RuntimeError before the correction.

The function now recognizes both the original and its precisely corrected label
block, and changes only that label rather than accepting an unrelated white
color elsewhere. It also avoids copying the logo when the source and installed
bytes are identical. The regression runs setup twice and checks the AuthUI,
GenericButton and logo bytes and modification times stay unchanged on the
second pass. No old files were deleted or timestamps repaired to hide changes.

All 134 backend tests passed in 12.629 seconds. The combined ISO static check
also passed; existing QML warnings remain. Red/green logs are retained in
`branding-repeat-logs/`. This fix is not yet part of rebuilt final media.

## Remaining package ownership work

The r9 online audit reports five altered theme files. The ownership causes are
not all in the same function:

- `GenericButton.qml`: package 44 lacks the installer-applied white label color.
- Lock-screen `images/branding.png`: the audit reports a timestamp mismatch;
  avoiding an identical copy addresses that redundant write on new runs.
- SDDM `background`, `default-background`, `preview.png`: the pinned Shell's
  `aero7_brand_sddm_background()` installs the ISO-generated Welcome image.
  Package 44 contains different background/preview content.

The active packaged SDDM Main.qml uses `Assets/aero7-branding-r3.png`; the Python
legacy-branding matcher does not match that reference. Do not incorrectly
attribute those SDDM background writes to `brand_sddm_themes()`.

The theme package must own the corrected button and intended Welcome assets
so upgrading cannot restore the older appearance. The pinned Shell's unconditional
background copy remains a separate metadata/idempotency consideration. Do not
claim whole-theme package integrity, update-survival or fresh-media acceptance
from the repeat-setup unit test. A normal package upgrade and subsequent setup,
login and lock-screen checks remain required.

The intended Welcome image has identical bytes in both r9 generated profiles:
`65e825c2dcc1b0c80d14896a6108199d825f8dc7b44724f22fe19d8b308fb7e7`.
It is the existing `usr/share/aero7/branding/aero7-login-background.jpg`, not new
artwork. A future theme package must include this exact approved image and the
specific white `btnLabel` correction. The package-44 AuthUI already uses
`Image.PreserveAspectFit` for the corrected logo; retain that existing sizing.
The pinned Shell also creates `bgtexture.jpg`, which is not one of the five
altered package-owned files in the r9 audit. Its unconditional `install -m 0644`
can still change modification times even after package content matches. Keep
that metadata-only distinction visible rather than claiming zero alterations.
