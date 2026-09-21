# Update preference and approval checks — 8 September 2026

Scope: the existing r10 offline installation, Control Panel 50, with the
previously tested Programs Center 3 and Paint 9 component upgrades. The VM
remained disconnected (`-nic none`, only loopback). No installed product
package was changed during this pass. Frozen r10 images remain unchanged.

## Installed UI checks

1. First-run preference was `recommended`, with no per-user override. The
   notification-only timer was enabled and active.
2. In Control Panel → Windows Update → Change settings, unchecked **Check for
   updates automatically and notify me**, then saved. Reopening showed off.
3. Checked it again but chose **Cancel**. Closed and relaunched Control Panel;
   the checkbox was still off. The actual user configuration contained
   `Enabled=false`. Running the installed helper returned successfully with
   `Automatic update checks are off`.
4. While automatic checking was off, clicked **Check for updates**. The
   disconnected guest displayed **Could not check for updates**, explicitly
   saying no updates were installed. It did not claim to be up to date.
5. Enabled checks and saved. The user configuration contained `Enabled=true`.
6. Performed a normal guest reboot and password login. Reopened the settings:
   the checkbox remained enabled, the timer was active/enabled, and both
   system and user failed-unit lists were empty. The package list still
   matched baseline. Screenshot 103 and `update-preference-reboot.log` record
   this result. OFF persistence was checked across application relaunch, not
   a separate reboot with the setting off.

The timer deliberately stays enabled when checks are off: its helper reads the
user preference and exits before probing. Do not describe this as disabling
the systemd timer or permitting unattended installations.

Evidence: `r10-update-logs/update-preference-{baseline,off,on}.log`, corresponding
complete package lists, and screenshots 94–97. The package lists are identical.

## Source regression and real Wayland replay

Added repository and AUR rows exercising the actual **Install updates?**
confirmation dialog. Each asserts that **No** is the default and declining
starts no installation command. Commands are harmless temporary fixtures;
the test never invokes real privileged or package-management operations.

The first test attempt incorrectly counted the AUR read-only `-Si` metadata
lookup as an install. Correcting that fixture resolved the failure; no runtime
product fix was needed. The completed suite passed **20/20** locally using
Qt's offscreen platform and **20/20** as an unprivileged process in the VM's
actual Wayland session. Existing cases also cover transaction window-close
protection, failed command starts, failed check results, and toggle persistence.
The notification-helper Python suite passed **15/15**.

These standalone test binaries emit missing-pack-icon warnings, and the host
offscreen run emits platform warnings. They are not a warning-free visual
acceptance result. Actual installed UI screenshots show the corresponding
status icons. Successful real repository/AUR upgrades were not attempted on
this disconnected guest.

Logs: `r10-update-logs/update-settings-source-test.txt` and
`r10-update-logs/update-settings-wayland-test.txt`.

## Release boundary

This is a bounded update-settings pass, not full Beta 2 acceptance. Online
transaction coverage, final-image compatibility checks, other application and
recovery gates remain. No commit, push, ISO rebuild or publication was made.
