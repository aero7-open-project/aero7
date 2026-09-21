import sys
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
import xml.etree.ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from firewall_defaults import (prepare_fresh_firewall, activate_selected_firewall,
                               choose_current_connection, apply_network_location, ZONE_XML, ZONES,
                               INFORMATION_RULE, INFORMATION_RULE_PATH)


class FirewallDefaultsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.write("etc/os-release", "NAME=Aero7\n")
        self.runner = Mock()

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding="utf-8")
        return path

    def test_fresh_configuration_validated_before_backend_marker(self):
        marker = self.root / "etc/aero7/firewall-backend"
        self.runner.run.side_effect = lambda args: self.assertFalse(marker.exists())
        self.assertTrue(prepare_fresh_firewall(self.root, self.runner))
        self.assertEqual(marker.read_text(), "firewalld\n")
        policy = self.root / INFORMATION_RULE_PATH
        self.assertEqual(policy.read_text(), INFORMATION_RULE)
        self.assertEqual(policy.stat().st_mode & 0o777, 0o644)
        prefix = ["arch-chroot", str(self.root)]
        self.assertEqual([call.args[0] for call in self.runner.run.call_args_list], [
            prefix + ["firewall-offline-cmd", "--set-default-zone=aero7-public"],
            prefix + ["firewall-offline-cmd", "--check-config"],
            prefix + ["systemctl", "enable", "firewalld.service"],
        ])

    def test_no_ssh_sharing_or_forwarding_opened(self):
        zone = ET.fromstring(ZONE_XML)
        self.assertEqual(zone.attrib, {})
        self.assertEqual([(child.tag, child.attrib) for child in zone
                          if child.tag not in {"short", "description"}],
                         [("service", {"name": "dhcpv6-client"})])

    def test_host_root_rejected(self):
        with self.assertRaises(ValueError):
            prepare_fresh_firewall(Path("/"), self.runner)
        self.runner.run.assert_not_called()

    def test_information_rule_does_not_replace_custom_policy_or_symlinks(self):
        policy = self.write(INFORMATION_RULE_PATH, "// Administrator policy\n")
        with self.assertRaisesRegex(ValueError, "refusing overwrite"):
            prepare_fresh_firewall(self.root, self.runner)
        self.assertEqual(policy.read_text(), "// Administrator policy\n")
        policy.unlink()
        policy.symlink_to(self.root / "outside.rules")
        with self.assertRaisesRegex(ValueError, "refusing overwrite"):
            prepare_fresh_firewall(self.root, self.runner)
        self.assertFalse((self.root / "outside.rules").exists())
        self.runner.run.assert_not_called()

    def test_information_rule_only_authorizes_local_active_read_actions(self):
        node = shutil.which("node")
        self.assertIsNotNone(node, "Node.js is required to execute the actual polkit rule test")
        actions = ["config.info", "direct.info", "policies.info", "all", "config",
                   "direct", "policies", "config.info.extra", "info"]
        cases = []
        for local in (True, False):
            for active in (True, False):
                for suffix in actions:
                    cases.append({"id": "org.fedoraproject.FirewallD1." + suffix,
                                  "local": local, "active": active,
                                  "expected": local and active and suffix in
                                      {"config.info", "direct.info", "policies.info"}})
        cases.append({"id": "org.example.config.info", "local": True,
                      "active": True, "expected": False})
        script = """
let rule;
global.polkit = {Result: {YES: 'yes'}, addRule: fn => {rule = fn;}};
""" + INFORMATION_RULE + """
for (const c of JSON.parse(process.argv[1])) {
    const actual = rule({id: c.id}, {local: c.local, active: c.active});
    if ((actual === 'yes') !== c.expected || (!c.expected && actual !== undefined))
        throw new Error(JSON.stringify({c, actual}));
}
"""
        subprocess.run([node, "-e", script, json.dumps(cases)], check=True,
                       capture_output=True, text=True)

    def test_enabled_and_disabled_ufw_are_preserved(self):
        for state in ("yes", "no"):
            with self.subTest(state=state):
                config = self.write("etc/ufw/ufw.conf", f"ENABLED={state}\n")
                self.assertFalse(prepare_fresh_firewall(self.root, self.runner))
                self.assertFalse(activate_selected_firewall(self.runner, self.root))
                self.assertEqual(config.read_text(), f"ENABLED={state}\n")
                self.assertFalse((self.root / INFORMATION_RULE_PATH).exists())
        self.runner.run.assert_not_called()

    def test_existing_backend_and_custom_zone_preserved(self):
        self.write("etc/aero7/firewall-backend", "firewalld\n")
        zone = self.write("etc/firewalld/zones/aero7-public.xml", "custom")
        self.assertFalse(prepare_fresh_firewall(self.root, self.runner))
        self.assertEqual(zone.read_text(), "custom")
        self.runner.run.assert_not_called()

    def test_partial_retry_does_not_overwrite_different_zone(self):
        zone = self.write("etc/firewalld/zones/aero7-public.xml", "custom")
        with self.assertRaisesRegex(ValueError, "refusing overwrite"):
            prepare_fresh_firewall(self.root, self.runner)
        self.assertEqual(zone.read_text(), "custom")
        self.runner.run.assert_not_called()

    def test_failure_never_marks_success(self):
        self.runner.run.side_effect = RuntimeError("configuration rejected")
        with self.assertRaises(RuntimeError):
            prepare_fresh_firewall(self.root, self.runner)
        self.assertFalse((self.root / "etc/aero7/firewall-backend").exists())

    def test_only_explicit_firewalld_is_activated(self):
        self.write("etc/aero7/firewall-backend", "firewalld\n")
        self.assertTrue(activate_selected_firewall(self.runner, self.root))
        self.assertEqual([call.args[0] for call in self.runner.run.call_args_list], [
            ["systemctl", "enable", "--now", "firewalld.service"],
            ["firewall-cmd", "--state"],
        ])

    def test_competing_ufw_fails_without_any_change(self):
        self.write("etc/aero7/firewall-backend", "firewalld\n")
        self.write("etc/ufw/ufw.conf", "ENABLED=yes\n")
        with self.assertRaisesRegex(ValueError, "competing"):
            activate_selected_firewall(self.runner, self.root)
        self.runner.run.assert_not_called()

    def test_unknown_backend_rejected(self):
        self.write("etc/aero7/firewall-backend", "typo\n")
        with self.assertRaises(ValueError):
            activate_selected_firewall(self.runner, self.root)
        self.runner.run.assert_not_called()

    def test_activation_failure_is_not_hidden(self):
        self.write("etc/aero7/firewall-backend", "firewalld\n")
        self.runner.run.side_effect = RuntimeError("service failed")
        with self.assertRaises(RuntimeError):
            activate_selected_firewall(self.runner, self.root)

    def network_query(self, entries, saved_zone="aero7-home"):
        def query(arguments):
            field = arguments[1]
            if field == "UUID":
                return "\n".join(entries)
            entry = entries[arguments[-1]]
            if field == "connection.type":
                return entry[0]
            if field == "GENERAL.DEFAULT,GENERAL.DEFAULT6":
                return entry[1]
            if field == "connection.zone":
                return saved_zone
            raise AssertionError(arguments)
        return query

    def test_network_selection_ignores_vpn_and_loopback(self):
        ids = [f"00000000-0000-0000-0000-{index:012d}" for index in range(3)]
        query = self.network_query({ids[0]: ("802-11-wireless", "yes\nno"),
                                    ids[1]: ("vpn", "yes\nyes"),
                                    ids[2]: ("loopback", "no\nno")})
        self.assertEqual(choose_current_connection(query), ids[0])

    def test_no_connection_does_not_assign_future_trust(self):
        self.write("etc/aero7/firewall-backend", "firewalld\n")
        self.assertEqual(apply_network_location("home", self.runner, self.root,
                                               self.network_query({})),
                         "public-default-no-unambiguous-connection")
        self.runner.run.assert_not_called()

    def test_split_ipv4_ipv6_defaults_are_not_guessed(self):
        query = self.network_query({
            "00000000-0000-0000-0000-000000000001": ("802-3-ethernet", "yes\nno"),
            "00000000-0000-0000-0000-000000000002": ("802-11-wireless", "no\nyes"),
        })
        self.assertIsNone(choose_current_connection(query))

    def test_one_local_network_can_be_selected_without_default_route(self):
        uuid = "00000000-0000-0000-0000-000000000001"
        self.assertEqual(choose_current_connection(self.network_query({uuid: ("802-3-ethernet", "no\nno")})), uuid)

    def test_home_only_modifies_selected_uuid(self):
        uuid = "00000000-0000-0000-0000-000000000001"
        self.write("etc/aero7/firewall-backend", "firewalld\n")
        query = self.network_query({uuid: ("802-3-ethernet", "yes\nno")})
        self.assertEqual(apply_network_location("home", self.runner, self.root, query), "connection-location-applied")
        self.runner.run.assert_called_once_with([
            "nmcli", "--wait", "10", "connection", "modify", "uuid", uuid,
            "connection.zone", "aero7-home"])

    def test_legacy_network_selection_does_not_query_or_mutate(self):
        query = Mock(side_effect=AssertionError("must not query"))
        self.assertEqual(apply_network_location("home", self.runner, self.root, query), "existing-firewall-preserved")
        self.runner.run.assert_not_called()

    def test_network_verification_failure_is_reported(self):
        uuid = "00000000-0000-0000-0000-000000000001"
        self.write("etc/aero7/firewall-backend", "firewalld\n")
        query = self.network_query({uuid: ("802-3-ethernet", "yes\nno")}, "public")
        with self.assertRaisesRegex(RuntimeError, "verified"):
            apply_network_location("home", self.runner, self.root, query)

    def test_changing_network_is_rejected_before_modification(self):
        self.write("etc/aero7/firewall-backend", "firewalld\n")
        from unittest.mock import patch
        with patch("firewall_defaults.choose_current_connection", side_effect=["one", "two"]):
            with self.assertRaisesRegex(ValueError, "changed"):
                apply_network_location("work", self.runner, self.root)
        self.runner.run.assert_not_called()

    def test_public_work_do_not_enable_discovery_or_sharing(self):
        for name in ("aero7-public", "aero7-work"):
            self.assertEqual([item.attrib["name"] for item in ET.fromstring(ZONES[name]).findall("service")],
                             ["dhcpv6-client"])
        self.assertEqual([item.attrib["name"] for item in ET.fromstring(ZONES["aero7-home"]).findall("service")],
                         ["dhcpv6-client", "mdns"])
