# First Boot and OOBE

The first installed boot starts a one-time Cage/Qt setup service instead of a
normal desktop login. The final Beta 2 flow opens directly on account setup;
the old separate “applying settings” and “checking video performance” pages
are no longer part of the published sequence.

## Personalization pages

1. **User and computer name** — creates the normal Linux account and hostname.
2. **Password** — requires matching values and applies the account password.
3. **Update preference** — records the selected update policy.
4. **Time and date** — chooses the system time zone.
5. **Network location** — stores the selected network profile intent.
6. **Finalizing** — applies the Aero7-shell image-mode configuration.

| Account and computer name | Password |
| --- | --- |
| ![Account and computer name](images/oobe-03-account.png) | ![Account password](images/oobe-04-password.png) |

| Update preference | Date, time, and time zone |
| --- | --- |
| ![Update preference](images/oobe-05-updates.png) | ![Date and time](images/oobe-06-time.png) |

| Network location | Finalizing settings |
| --- | --- |
| ![Network location](images/oobe-07-network.png) | ![Finalizing settings](images/oobe-08-finalizing.png) |

## Desktop preparation

OOBE applies the light Aero color scheme, wallpaper, Start menu, single Aero
taskbar, window decorations, icons, sounds, SDDM branding, application names,
and first-login repair service. The system then shows Welcome and Preparing
your desktop before starting Plasma directly—there is no second reboot and no
manual Continue button.

| Welcome | Preparing your desktop |
| --- | --- |
| ![Welcome transition](images/oobe-09-welcome.png) | ![Preparing the desktop](images/oobe-10-preparing-desktop.png) |

![Desktop handoff](images/oobe-11-desktop-handoff.png)

## One-time automatic login

The first desktop session logs in automatically so the transition feels
continuous. A self-disabling cleanup timer removes that temporary SDDM setting
after 45 seconds. Later boots require the account password normally. The
22 September gallery captures this exact final-ISO flow at 1920×1080.

## User name rules

Use a normal Linux account name: lower-case letters and digits are safest. Do
not use `root` or an existing system account. The computer name must be a valid
hostname and must not contain spaces.

## Recovery

If OOBE cannot finish, switch to TTY2 with Alt+F2 and inspect the commands in
[Recovery and Logs](Recovery-and-Logs.md). The one-time service remains
diagnosable and does not
create a passwordless sudo rule.
