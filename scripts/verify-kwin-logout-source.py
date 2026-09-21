#!/usr/bin/env python3
"""Source-policy guard for the KWin candidate; not a runtime acceptance test."""
import re
import sys
from pathlib import Path


def verify(root: Path) -> None:
    source = (root / "src/sm.cpp").read_text()
    header = (root / "src/sm.h").read_text()
    close = source.split("bool SessionManager::closeWaylandWindows()", 1)[1].split(
        "void SessionManager::updateWaylandCancelNotification()", 1
    )[0]
    assert "m_logoutAnywayTimer" not in source + header, "Unconditional force timer remains"
    assert "Logging out anyway in 2 minutes." not in source, "Stale countdown text"
    assert "may discard unsaved work" in source, "Explicit override needs data-loss warning"
    assert 'i18nc("@action:button", "Cancel Logout")' in close
    assert 'i18nc("@action::button", "Log Out Anyway")' in close
    for signal in ("cancel, &KNotificationAction::activated", "m_cancelNotification, &KNotification::closed"):
        handler = close.split("connect(" + signal, 1)[1].split("});", 1)[0]
        assert "createReply(false)" in handler, f"{signal} must reject logout"
        assert "createReply(true)" not in handler
    override = close.split("connect(quit, &KNotificationAction::activated", 1)[1].split("});", 1)[0]
    assert "createReply(true)" in override, "Explicit override was removed"
    # Successful replies are permitted only for the two no-pending-window paths
    # and the explicit user action. This is a structural guard, not a C++ proof.
    assert len(re.findall(r"createReply\(true\)", close)) == 3
    assert "if (m_pendingWindows.empty())" in close
    assert "Operation already in progress" in close
    completed = close.split("if (m_pendingWindows.empty())", 1)[1].split("} else {", 1)[0]
    assert completed.index("m_closingWindowsGuard.reset()") < completed.index("m_cancelNotification->close()"), \
        "Disconnect cancellation before programmatic notification cleanup"
    fallback = close.split("#else", 1)[1].split("#endif", 1)[0]
    assert "createReply(false)" in fallback, "No-notification builds must fail closed"
    print("KWIN_LOGOUT_SOURCE_POLICY_PASS (runtime tests still required)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: verify-kwin-logout-source.py PREPARED_KWIN_SOURCE")
    verify(Path(sys.argv[1]))
