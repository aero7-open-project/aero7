"""Fresh-target firewalld setup. Never migrate an existing UFW installation.

This module is called only by the fresh-install path, not package upgrades.
OOBE uses the explicit backend marker and does not infer migration permission
from the mere presence of the firewalld package.
"""

from pathlib import Path
import re
import subprocess


ZONE_NAME = "aero7-public"
# Firewalld's Arch server policy authenticates configuration-information reads
# such as the denied-packet logging setting shown in Control Panel. Permit only
# information access for a local active desktop session, never configuration
# changes or the umbrella "all" action. Package-owned policy stays untouched.
INFORMATION_RULE_PATH = "etc/polkit-1/rules.d/49-aero7-firewall-information.rules"
INFORMATION_RULE = '''// Aero7 fresh-install desktop: read-only firewall information.
polkit.addRule(function(action, subject) {
    if (subject.local === true && subject.active === true &&
        (action.id === "org.fedoraproject.FirewallD1.config.info" ||
         action.id === "org.fedoraproject.FirewallD1.direct.info" ||
         action.id === "org.fedoraproject.FirewallD1.policies.info")) {
        return polkit.Result.YES;
    }
});
'''
ZONE_XML = '''<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Aero7 Public</short>
  <description>Block unsolicited incoming traffic. Allow outgoing connections
  and their replies. No SSH or file sharing is opened automatically.</description>
  <service name="dhcpv6-client"/>
</zone>
'''
ZONES = {
    "aero7-public": ZONE_XML,
    "aero7-home": '''<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Aero7 Home</short>
  <description>Trusted home network: allow local mDNS discovery. File sharing
  and remote access still require explicit configuration.</description>
  <service name="dhcpv6-client"/>
  <service name="mdns"/>
</zone>
''',
    "aero7-work": '''<?xml version="1.0" encoding="utf-8"?>
<zone>
  <short>Aero7 Work</short>
  <description>Work network: block unsolicited incoming traffic. Add only
  the services approved for this workplace.</description>
  <service name="dhcpv6-client"/>
</zone>
''',
}


def prepare_fresh_firewall(target: Path, runner) -> bool:
    """Configure an explicitly fresh target; return False for existing setups.

    The target must be a mounted installation root, never the running host.
    Retry does not rewrite administrator rules. Configuration validation and
    service enablement must succeed before recording the selected backend.
    """
    target = target.resolve()
    if target == Path("/") or not (target / "etc/os-release").exists():
        raise ValueError("firewall setup requires a populated, non-host target")
    marker = target / "etc/aero7/firewall-backend"
    ufw_config = target / "etc/ufw/ufw.conf"
    # Even a disabled, existing UFW configuration belongs to its owner.
    # Fresh images must no longer install UFW before reaching this function.
    if marker.exists() or ufw_config.exists():
        return False
    information_rule = target / INFORMATION_RULE_PATH
    if information_rule.is_symlink() or (information_rule.exists() and
            information_rule.read_text(encoding="utf-8") != INFORMATION_RULE):
        raise ValueError("existing firewall information policy differs; refusing overwrite")
    # A partial install retry may have written our zone, but never overwrite
    # a differing user definition under the same name.
    for name, contents in ZONES.items():
        zone = target / f"etc/firewalld/zones/{name}.xml"
        if zone.exists() and zone.read_text(encoding="utf-8") != contents:
            raise ValueError("existing Aero7 firewall zone differs; refusing overwrite")
    for name, contents in ZONES.items():
        zone = target / f"etc/firewalld/zones/{name}.xml"
        zone.parent.mkdir(parents=True, exist_ok=True)
        zone.write_text(contents, encoding="utf-8")
    prefix = ["arch-chroot", str(target)]
    information_rule.parent.mkdir(parents=True, exist_ok=True)
    information_rule.write_text(INFORMATION_RULE, encoding="utf-8")
    information_rule.chmod(0o644)
    runner.run(prefix + ["firewall-offline-cmd", f"--set-default-zone={ZONE_NAME}"])
    runner.run(prefix + ["firewall-offline-cmd", "--check-config"])
    runner.run(prefix + ["systemctl", "enable", "firewalld.service"])
    marker.parent.mkdir(parents=True, exist_ok=True)
    marker.write_text("firewalld\n", encoding="utf-8")
    return True


def query_network(arguments):
    result = subprocess.run(["nmcli", "--wait", "10", *arguments], check=True,
                            capture_output=True, text=True, timeout=15,
                            env={"PATH": "/usr/bin", "LC_ALL": "C.UTF-8"})
    return result.stdout.strip()


def choose_current_connection(query=query_network):
    """Return one unambiguous physical NM connection, never a VPN or loopback.

    Split IPv4/IPv6 default routes or multiple equally plausible connections
    are deliberately not guessed. An offline machine keeps the Public default;
    a later, unrelated network must not inherit today's Home selection.
    """
    candidates, defaults = [], []
    for connection in query(["--get-values", "UUID", "connection", "show", "--active"]).splitlines():
        if not re.fullmatch(r"[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}", connection):
            raise ValueError("NetworkManager returned an invalid connection UUID")
        if query(["--get-values", "connection.type", "connection", "show", "uuid", connection]) not in {
            "802-3-ethernet", "802-11-wireless",
        }:
            continue
        candidates.append(connection)
        primary = query(["--get-values", "GENERAL.DEFAULT,GENERAL.DEFAULT6",
                         "connection", "show", "uuid", connection]).splitlines()
        if "yes" in primary:
            defaults.append(connection)
    if len(defaults) == 1:
        return defaults[0]
    if not defaults and len(candidates) == 1:
        return candidates[0]
    return None


def apply_network_location(location, runner, root=Path("/"), query=query_network):
    """Persist the first-run location only on the currently selected connection."""
    if location not in {"home", "work", "public", "wired", "skip"}:
        raise ValueError("Invalid network location")
    marker = root / "etc/aero7/firewall-backend"
    if not marker.exists() or marker.read_text().strip() != "firewalld":
        return "existing-firewall-preserved"
    if location == "skip":
        return "public-default-no-selection"
    selected = choose_current_connection(query)
    if selected is None:
        return "public-default-no-unambiguous-connection"
    # Detect a changing connection before making any persistent trust change.
    if choose_current_connection(query) != selected:
        raise ValueError("The active network changed; select its location again")
    zone = "aero7-" + ("public" if location == "wired" else location)
    runner.run(["nmcli", "--wait", "10", "connection", "modify", "uuid", selected,
                "connection.zone", zone])
    # NM applies zone updates immediately, without disconnecting the device.
    if query(["--get-values", "connection.zone", "connection", "show", "uuid", selected]) != zone:
        raise RuntimeError("Network location could not be verified after saving")
    return "connection-location-applied"


def activate_selected_firewall(runner, root: Path = Path("/")) -> bool:
    """Start only an explicitly selected firewalld backend at first login.

    No marker means legacy installation: leave all UFW rules, enabled state,
    and services untouched. Do not activate competing packet filters.
    """
    marker = root / "etc/aero7/firewall-backend"
    if not marker.exists():
        return False
    backend = marker.read_text(encoding="utf-8").strip()
    if backend == "ufw":
        return False
    if backend != "firewalld":
        raise ValueError("unrecognized selected firewall backend")
    ufw_config = root / "etc/ufw/ufw.conf"
    if ufw_config.exists() and re.search(
        r"^\s*ENABLED\s*=\s*yes\s*$",
        ufw_config.read_text(encoding="utf-8"), re.MULTILINE | re.IGNORECASE,
    ):
        raise ValueError("UFW is enabled; refusing to activate a competing firewall")
    runner.run(["systemctl", "enable", "--now", "firewalld.service"])
    runner.run(["firewall-cmd", "--state"])
    return True
