# Known Issues

## Beta 2 limitations

- The physical-hardware compatibility matrix is still limited. Beta 2 has a
  guarded installer, but unusual storage controllers, firmware, or graphics
  hardware may require the debug boot option or may not work yet.
- Only x86-64 UEFI is supported.
- The online ISO requires internet throughout package installation. The
  recommended offline ISO installs the base system without a connection, but
  later updates and some optional features still require repositories.
- Full-disk encryption, free-form manual partitioning and legacy BIOS are
  unavailable. RAID On/Intel RST disks may be invisible until firmware is
  safely changed to AHCI.
- Advanced mode currently installs its own Aero7 ESP. Existing firmware boot
  entries are preserved, so another OS may be selected through the firmware
  boot menu rather than the Aero7 systemd-boot menu.
- Language and regional choices are limited to the currently validated flow.

## Display and input

QEMU's legacy standard VGA output can miss wlroots damage updates, leaving mouse
trails or fragments of a previous page. Some GTK/Cairo combinations have also
shown a black window that repaints only when the pointer moves. Use QXL through
SPICE and a VirtIO tablet, as documented in
[System Requirements](System-Requirements.md).

The host SPICE viewer may print harmless GTK minimum-size or automount-inhibitor
warnings. These do not indicate a guest installer failure.

## First desktop session

Plasma may briefly react to a virtual display hotplug and open Display
Configuration on unusual host display changes. Close it normally. The Aero7
first-login helper also repairs duplicate panels, light colors, application
branding, and menu indexing once per account.

## Packaging

The online ISO consumes distribution packages during installation. A future
incompatible upstream package can therefore affect an unchanged online image.
The offline ISO uses its checksum-pinned embedded repository for the base
installation. Report the ISO variant, checksum, installer log and date when
filing a package failure.

## Licensing

PlymouthVista is included under its distributed MIT license. Aero7 replaces its
product logo, reveal, and branding frames with project artwork. See
[Credits and Licensing](Credits-and-Licensing.md) for the complete package and
third-party license list.
