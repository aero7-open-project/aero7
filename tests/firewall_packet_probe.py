#!/usr/bin/env python3
"""Manual QA only: isolated IPv4/IPv6 traffic probe in a disposable QEMU VM.

Run before activation with --expect-inbound allowed and after activation with
--expect-inbound blocked. Does not change UFW rules or the VM's real interfaces.
"""
import argparse
import json
import os
from pathlib import Path
import select
import socket
import subprocess
import sys
import uuid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--expect-inbound", choices=("allowed", "blocked"), required=True)
    parser.add_argument("--execute-in-disposable-vm", action="store_true", required=True)
    args = parser.parse_args()
    if os.geteuid() != 0 or "QEMU" not in Path("/sys/class/dmi/id/sys_vendor").read_text():
        raise SystemExit("Run only as root inside the disposable QEMU QA guest")
    token = uuid.uuid4().hex[:7]
    namespace, local, peer = "a7qa-" + token, "a7l" + token, "a7p" + token
    prefix = ["ip", "netns", "exec", namespace]
    created = False
    peers = []

    def run(argv):
        return subprocess.run(argv, check=True, text=True, capture_output=True)

    try:
        run(["ip", "netns", "add", namespace])
        created = True
        run(["ip", "link", "add", local, "type", "veth", "peer", "name", peer])
        run(["ip", "link", "set", peer, "netns", namespace])
        for command_prefix, interface, v4, v6 in [
            ([], local, "10.203.97.1/30", "fd7a:203:97::1/126"),
            (prefix, peer, "10.203.97.2/30", "fd7a:203:97::2/126"),
        ]:
            run(command_prefix + ["ip", "addr", "add", v4, "dev", interface])
            run(command_prefix + ["ip", "-6", "addr", "add", v6, "dev", interface, "nodad"])
            run(command_prefix + ["ip", "link", "set", interface, "up"])
        run(prefix + ["ip", "link", "set", "lo", "up"])

        for family, root_address, peer_address in [
            (socket.AF_INET, "10.203.97.1", "10.203.97.2"),
            (socket.AF_INET6, "fd7a:203:97::1", "fd7a:203:97::2"),
        ]:
            with socket.socket(family, socket.SOCK_STREAM) as listener:
                listener.bind((root_address, 19000))
                listener.listen(1)
                client_code = (
                    "import socket,sys; s=socket.socket(int(sys.argv[1]),socket.SOCK_STREAM); "
                    "s.settimeout(2); result=s.connect_ex((sys.argv[2],19000)); "
                    "print(result); sys.exit(0 if result == 0 else 1)"
                )
                inbound = subprocess.run(prefix + [sys.executable, "-c", client_code,
                    str(int(family)), root_address], text=True, capture_output=True, timeout=5)
                accepted = inbound.returncode == 0
                # An exception or namespace command failure must not count as a blocked packet.
                if inbound.returncode not in (0, 1) or not inbound.stdout.strip().isdigit():
                    raise RuntimeError(f"Invalid inbound probe: {inbound.stderr}")
                assert accepted == (args.expect_inbound == "allowed"), inbound.stdout

            server_code = (
                "import socket,sys; s=socket.socket(int(sys.argv[1]),socket.SOCK_STREAM); "
                "s.bind((sys.argv[2],19001)); s.listen(1); print('ready',flush=True); "
                "c,a=s.accept(); c.sendall(b'aero7-firewall-probe'); c.close()"
            )
            server = subprocess.Popen(prefix + [sys.executable, "-c", server_code,
                str(int(family)), peer_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True)
            peers.append(server)
            if not select.select([server.stdout], [], [], 5)[0] or server.stdout.readline().strip() != "ready":
                raise RuntimeError("Outbound fixture did not become ready")
            with socket.socket(family, socket.SOCK_STREAM) as client:
                client.settimeout(3)
                client.connect((peer_address, 19001))
                assert client.recv(64) == b"aero7-firewall-probe"
            assert server.wait(timeout=3) == 0
            print(json.dumps({"family": int(family), "inbound": args.expect_inbound,
                "outbound": "allowed", "reply_payload": "verified"}), flush=True)
    finally:
        for process in peers:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=3)
        if created:
            # Only this invocation's exact temporary namespace and interface.
            subprocess.run(["ip", "netns", "delete", namespace], check=False)
            subprocess.run(["ip", "link", "delete", local], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


if __name__ == "__main__":
    main()
