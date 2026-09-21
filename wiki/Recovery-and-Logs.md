# Recovery and Logs

## Physical-install diagnostic folder

Diagnostic test images place **Aero7 Physical Install Logs** on the installed
user's desktop after OOBE. Before sharing a report, double-click **Collect
Aero7 Logs Now** in that folder if the desktop is still usable. Wait for the
collection to finish, then copy the entire folder rather than one screenshot
of the last error. Keep the original until the report has been received.

System collection refreshes every ten minutes and desktop-session collection
every five minutes. Per-boot directories separate sessions, and a SHA-256
manifest helps check the returned collection. This folder is a diagnostic
test-media feature; do not assume an older ISO already contains it.

| Area | What it helps diagnose |
| --- | --- |
| Installer | Installer/OOBE output, storage actions, retained live-media logs, and installation source |
| System | Current/previous boot journals, kernel messages, failed services, mounts, memory, and disk space |
| Hardware | CPU, firmware, graphics, USB, storage health, networking, and detected devices |
| Packages | Installed versions, pacman history, repository configuration, and integrity results |
| Desktop/session | SDDM, Aero7 and user-session state, display information, and selected application logs |
| Crashes | Crash summaries without full process core-memory images |

The collector deliberately avoids copying passwords, NetworkManager
connection-profile files, browser data, personal document contents, and full
core images. **It is not a guarantee of anonymity:** journals and application
logs can contain account/computer names, disk serials, MAC addresses, network
names, file paths, or application-provided text. Review before sharing and
prefer a private transfer for sensitive diagnostics.

Include the ISO filename, online/offline edition, hardware model, approximate
failure time, visible error, and whether installation or first login had
completed. A screenshot alone does not show the complete dependency error.

## Open recovery

Press **Alt+F2** to switch to the recovery console. Press **Alt+F1** to return to
the graphical setup. On the Install now page, **Repair your computer** confirms
the action and performs the same TTY2 handoff.

## Live installer logs

```bash
journalctl -u aero7-installer --no-pager
cat /var/log/aero7-kiosk.log
cat /var/log/aero7-installer.log
```

Useful device information:

```bash
lsblk -o NAME,PATH,SIZE,TYPE,FSTYPE,MOUNTPOINTS,RO,RM,MODEL,SERIAL
findmnt
ip address
```

## First-boot logs

After the disk phase has succeeded:

```bash
journalctl -u aero7-oobe.service --no-pager
journalctl -u sddm.service --no-pager
cat /var/log/aero7-installer.log
```

The embedded shell state and logs are normally under `/var/lib/aero7` and the
selected user's Aero7 state directory. The exact signed package request is:

```text
/var/lib/aero7/requested-aero7-packages.txt
```

## Installed-system checks

Once the account is available:

```bash
aero7 status
aero7 doctor
aero7 repo status
aero7 apps status
```

## Safety warning

Do not copy commands from random recovery guides that disable signature checks,
erase a broader disk path, or install a passwordless sudo rule. Capture logs
first and file an issue when the correct recovery action is unclear.
