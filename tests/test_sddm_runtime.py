#!/usr/bin/env python3
"""Run actual greeter subtrees with isolated models, without starting SDDM.

The generated fixtures retain the theme's anchored geometry and button logic.
They do not authenticate, execute shell commands or change installed themes.
Pass a prepared theme directory containing Main.qml, SMOD/ and Assets/.
"""
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


def subtree(source, identifier):
    start = re.search(r"[\w.]+\s*\{\s*id:\s*" + re.escape(identifier) + r"\b", source)
    if start is None:
        raise ValueError(f"Missing QML object: {identifier}")
    depth = 0
    # Ignore braces in strings and comments rather than cutting at a JS block.
    tokens = r'''//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[{}]'''
    for token in re.finditer(tokens, source[start.start():]):
        if token.group() == "{":
            depth += 1
        elif token.group() == "}":
            depth -= 1
            if depth == 0:
                return source[start.start():start.start() + token.end()]
    raise ValueError(f"Unclosed QML object: {identifier}")


IMPORTS = '''import QtQuick
import QtQuick.Layouts
import QtQuick.Controls as QQC2
import Qt5Compat.GraphicalEffects
import org.kde.kirigami as Kirigami
import "SMOD" as SMOD
'''

MOCKS = '''
    property bool m_biggerUserFrame: false
    property bool m_biggerMultiUserFrame: false
    function i18nd(domain, text) { return text }
    function i18ndc(domain, context, text) { return text }
    QtObject { id: keyboard; property var layouts: []; property int currentLayout: 0; property bool capsLock: false }
    QtObject { id: pages; property int currentIndex: 2 }
    Item { id: listView; property int currentIndex: 0; property int cellWidth: 200; property int cellHeight: 200 }
    Item { id: accessbutton }
    Item { id: rebootButton }
'''

TESTS = '''import QtQuick
import QtTest

TestCase {
    name: "Aero7GreeterLayout"
    when: windowShown
    visible: true
    width: 1920; height: 1080
    Component { id: loginComponent; LoginFixture {} }
    Component { id: delegateComponent; DelegateFixture {} }
    function init() {
        failOnWarning(/.*(Cannot specify|managed by a layout|TypeError|ReferenceError|Binding loop).*/)
    }
    function test_loginGeometry_data() {
        return [
            {tag: "1080p-normal", bigger: false, w: 1920, h: 1080},
            {tag: "1080p-large", bigger: true, w: 1920, h: 1080},
            {tag: "laptop-normal", bigger: false, w: 1366, h: 768},
            {tag: "laptop-large", bigger: true, w: 1366, h: 768},
            {tag: "small-normal", bigger: false, w: 800, h: 600}]
    }
    function test_loginGeometry(data) {
        let f = createTemporaryObject(loginComponent, this, {m_biggerUserFrame: data.bigger, width: data.w, height: data.h})
        verify(f !== null)
        wait(30)
        compare(f.frame.x + f.frame.width / 2, f.width / 2)
        compare(f.frame.y + f.frame.height / 2, f.height / 2)
        compare(f.picture.width, data.bigger ? 238 : 190)
        compare(f.picture.y + f.picture.height, f.frame.height / 2 + (data.bigger ? 64 : 56))
        compare(f.userLabel.y, f.picture.y + f.picture.height)
        compare(f.loginBox.y, f.userLabel.y + f.userLabel.height + 8)
        compare(f.switchUser.y, f.picture.y + f.picture.height + 124)
    }
    function test_keyboardLifecycle() {
        let f = createTemporaryObject(loginComponent, this)
        verify(f !== null)
        wait(20)
        compare(f.layoutButton.text, "")
        verify(!f.layoutButton.visible)
        f.layoutButton.clicked()
        compare(f.keyboardModel.currentLayout, 0)
        f.keyboardModel.layouts = [{shortName: "us"}]
        compare(f.layoutButton.text, "us")
        verify(!f.layoutButton.visible)
        f.keyboardModel.layouts = [{shortName: "us"}, {shortName: "nl"}]
        compare(f.layoutButton.text, "us")
        verify(f.layoutButton.visible)
        f.layoutButton.clicked()
        compare(f.keyboardModel.currentLayout, 1)
        compare(f.layoutButton.text, "nl")
        f.keyboardModel.currentLayout = 0
        compare(f.layoutButton.text, "us")
        f.keyboardModel.currentLayout = -1
        compare(f.layoutButton.text, "")
        f.layoutButton.clicked()
        compare(f.keyboardModel.currentLayout, 0)
        f.keyboardModel.currentLayout = 99
        compare(f.layoutButton.text, "")
        f.layoutButton.clicked()
        compare(f.keyboardModel.currentLayout, 0)
        f.keyboardModel.layouts = []
        compare(f.layoutButton.text, "")
        f.layoutButton.clicked()
        compare(f.keyboardModel.currentLayout, 0)
    }
    function test_userDelegate_data() {
        return [{tag: "normal", bigger: false}, {tag: "large", bigger: true}]
    }
    function test_userDelegate(data) {
        let f = createTemporaryObject(delegateComponent, this, {m_biggerMultiUserFrame: data.bigger})
        verify(f !== null)
        wait(30)
        compare(f.frame.width, 200)
        compare(f.frame.height, 200)
        compare(f.picture.width, data.bigger ? 100 : 80)
        compare(f.picture.x + f.picture.width / 2, 100)
        compare(f.picture.y + f.picture.height / 2, 100)
    }
}
'''


def main():
    theme = Path(sys.argv[1]).resolve(strict=True)
    source = (theme / "Main.qml").read_text()
    login = subtree(source, "mainColumn")
    switch = subtree(source, "switchLayoutButton")
    delegate = subtree(source, "delegateColumn")
    with tempfile.TemporaryDirectory(prefix="aero7-sddm-runtime-") as temporary:
        directory = Path(temporary)
        for name in ("SMOD", "Assets"):
            (directory / name).symlink_to(theme / name, target_is_directory=True)
        enums = "enum LoginPage { Startup, SelectUser, Login, LoginFailed }"
        aliases = '''property alias frame: mainColumn
        property alias picture: userpic
        property alias userLabel: userNameLabel
        property alias loginBox: loginbox
        property alias switchUser: switchuser
        property alias keyboardModel: keyboard
        property alias layoutButton: switchLayoutButton
        '''
        (directory / "LoginFixture.qml").write_text(
            IMPORTS + "Item { width: 1920; height: 1080\n" + enums + MOCKS + aliases
            + login.replace("Main.", "LoginFixture.") + switch.replace("Main.", "LoginFixture.") + "\n}")
        (directory / "DelegateFixture.qml").write_text(
            IMPORTS + "Item { width: 200; height: 200\n" + MOCKS
            + 'property var model: ({realName: "Test User", name: "test", icon: "Assets/user.png"})\n'
            + "property alias frame: delegateColumn\nproperty alias picture: avatarparent\n"
            + delegate + "\n}")
        (directory / "tst_layout.qml").write_text(TESTS)
        env = dict(os.environ, QT_QPA_PLATFORM="offscreen", QT_QUICK_BACKEND="software", QT_FORCE_STDERR_LOGGING="1",
                   XDG_CONFIG_HOME=str(directory / "config"), XDG_CACHE_HOME=str(directory / "cache"))
        result = subprocess.run(["/usr/lib/qt6/bin/qmltestrunner", "-input", str(directory)], env=env, timeout=60)
        if result.returncode:
            return result.returncode
    userlist = subtree(source, "userlistpage")
    assert not re.search(r"id:\s*userlistpage\s+anchors\.fill:", userlist), "StackLayout child must not use fill anchors"
    print("SDDM_SUBTREE_GEOMETRY_AND_KEYBOARD_TESTS_PASSED_NOT_FULL_GREETER_ACCEPTANCE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
