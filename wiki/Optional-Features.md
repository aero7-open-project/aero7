# Aero7 Optional Features

Open **Start > Turn Aero7 features on or off**, or use **Control Panel >
Programs > Programs and Features > Turn Aero7 features on or off**. These are
real package and service controls, not cosmetic check boxes.

| Feature | Purpose and behavior |
| --- | --- |
| Aero7 Desktop Core | Required desktop session, shell, Control Panel and File Explorer. It cannot be removed. |
| Programs Center Beta | Optional graphical software manager. It is not installed by default. Both Beta 2 ISO variants retain its checksum-verified package locally, so it can be enabled offline and removed independently. |
| Encrypted Credential Vault | Optional and off by default. Adds Credential Manager for generic usernames/passwords using KWallet encryption and password prompts. Enable it, sign out and back in, then open Credential Manager. Use a non-empty vault password. Removal retains the encrypted files and account settings; re-enabling requires the original password. |
| Parental Controls | Installs `malcontent` for application restrictions on managed accounts; sign out after enabling it. |
| Backup and Restore | Installs Déjà Dup for scheduled personal-file backups and restores. Archives and settings are retained on removal. |
| System Recovery | Installs Snapper and Btrfs Assistant for snapshots; available only on Btrfs roots. Snapshots are retained on removal. |
| Advanced Accessibility Services | Installs Orca, Speech Dispatcher and eSpeak NG for screen reading and spoken feedback; sign out after enabling it. |
| Speech Recognition | Unavailable until Aero7 has a supported voice-control and dictation backend. Speech synthesis is not presented as recognition. |
| Sync Center | Installs Syncthing with a system-managed service instance for the account for trusted folder synchronization. Synced data and settings are retained. |
| Aero7 Defender | Installs ClamAV and its signature-update service for on-demand malware scanning. Signature data is retained. |
| Windows CardSpace | Hidden and unavailable because the historical Microsoft technology was discontinued and has no safe Aero7 equivalent. |
| Remote Desktop Connections | Installs the FreeRDP client. It does not enable incoming remote access. |
| File and Printer Sharing | Installs Samba and enables SMB services. No shares are created automatically; existing configuration is retained. |
| Mobile Broadband and Modem Support | Installs and enables ModemManager. It reports hardware not present when no compatible modem is detected. |
| Color Management | Installs colord for ICC profiles and color-corrected workflows; sign out after enabling it. Profiles are retained. |

Checked means installed. Unchecked means available but absent. A partial state
can be repaired by selecting the feature. Hardware-dependent and unavailable
entries explain their limitation. Aero7 asks for administrator approval before
making changes and never restarts automatically.

The catalog has 15 entries, including the protected desktop core and hidden
CardSpace entry. Only 13 are searchable optional features. An unavailable entry
is not a promise of an installable backend. Other than the specifically bundled
Programs Center and vault packages, optional features may require internet and
available repository packages. Downloading additional software or updating
malware signatures still requires connectivity.

The vault does not import browser passwords, autofill applications, implement
Windows domain credentials or encrypt the whole disk. It has no password recovery
or plaintext-export feature. Passwords are masked until explicitly revealed.
Sign out after disabling it; package removal preserves data and does not prove
that a running backend has stopped. Existing account wallet/portal overrides take
priority. If locking cannot be verified, credentials are hidden locally and you
should sign out before leaving the computer; a hidden window is not proof of a
successful backend lock.

Read the [complete Control Panel feature guide](https://github.com/aero7-open-project/aero7-control-panel-/wiki/Optional-Features)
for each backend, offline-cache limits, transaction steps, and failure reports.
The [Beta 2 desktop guide](Beta-2-Desktop-Guide) explains how these optional
features differ from the required desktop and companion applications.
