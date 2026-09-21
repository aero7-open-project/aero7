import QtQuick
import QtQuick.Controls

Dialog {
    id: dialog
    property string message: ""
    parent: Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(620, parent ? parent.width - 32 : 620)
    modal: true
    focus: true
    closePolicy: Popup.CloseOnEscape
    padding: 20
    onOpened: closeButton.forceActiveFocus()

    background: Rectangle {
        color: "#f7f9fc"
        border.color: "#718da8"
        radius: 4
    }
    header: Rectangle {
        implicitHeight: 38
        gradient: Gradient {
            GradientStop { position: 0; color: "#d9e9f7" }
            GradientStop { position: 1; color: "#b3cce5" }
        }
        Text {
            anchors.fill: parent
            anchors.leftMargin: 16
            anchors.rightMargin: 16
            verticalAlignment: Text.AlignVCenter
            text: dialog.title
            color: "#153c64"
            font.pixelSize: 15
        }
    }
    contentItem: Text {
        text: dialog.message
        wrapMode: Text.WordWrap
        textFormat: Text.PlainText
        color: "#263640"
        font.pixelSize: 13
        Accessible.role: Accessible.StaticText
        Accessible.name: text
    }
    footer: Item {
        implicitHeight: 55
        AeroButton {
            id: closeButton
            objectName: "setupHelpClose"
            anchors.right: parent.right
            anchors.rightMargin: 16
            anchors.verticalCenter: parent.verticalCenter
            text: qsTr("Close")
            onClicked: dialog.close()
        }
    }
}
