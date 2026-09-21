import QtQuick
import QtQuick.Controls

Button {
    id: control
    flat: true
    padding: 0
    implicitHeight: 24
    implicitWidth: label.implicitWidth
    focusPolicy: Qt.StrongFocus
    font.pixelSize: 12
    background: Item {}
    contentItem: Text {
        id: label
        text: control.text
        color: "#0067b1"
        font.family: control.font.family
        font.pixelSize: control.font.pixelSize
        font.underline: control.hovered || control.activeFocus
        verticalAlignment: Text.AlignVCenter
    }
}
