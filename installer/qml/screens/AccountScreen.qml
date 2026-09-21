import QtQuick
import "../components"

SetupPage {
    id: root
    anchors.fill: parent
    title: ""
    description: ""
    showHeading: false
    showBack: false

    body: [
        Brand {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 34
            width: 390
            height: 94
            markSize: 72
            titleSize: 38
            edition: qsTr("Professional")
            titleColor: "#1f252a"
            titleStyleColor: "#d9ffffff"
        },

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 127
            text: qsTr("Choose a user name for your account and name your computer to identify it on the network.")
            color: "#30373c"
            font.pixelSize: 12
        },

        Column {
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.top: parent.top
            anchors.topMargin: 168
            width: 380
            spacing: 4

            Text { text: qsTr("Type a user name (for example, Alex):"); color: "#25323b"; font.pixelSize: 12 }
            AeroTextField {
                width: parent.width
                text: root.controller.username
                placeholderText: qsTr("user name")
                onTextChanged: root.controller.username = text
            }
            Item { width: 1; height: 5 }
            Text { text: qsTr("Type a computer name:"); color: "#25323b"; font.pixelSize: 12 }
            AeroTextField {
                width: parent.width
                text: root.controller.computerName
                placeholderText: qsTr("aero7-pc")
                onTextChanged: root.controller.computerName = text
            }
        }
    ]
}
