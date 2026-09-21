pragma ComponentBehavior: Bound
import QtQuick
import "../components"

SetupPage {
    id: root
    anchors.fill: parent
    title: qsTr("Choose how Aero7 checks for updates")
    description: ""
    showBack: true
    showNext: false
    showFooter: false

    body: [
        Column {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            spacing: 4

            Repeater {
                model: [
                    { key: "recommended", icon: "shield-recommended.svg", title: qsTr("Check automatically and notify me (recommended)"), detail: qsTr("Check daily while signed in. You review and approve updates before anything is installed.") },
                    { key: "manual", icon: "shield-manual.svg", title: qsTr("Turn automatic checks off"), detail: qsTr("Check manually in Control Panel. You can turn automatic checks on again at any time.") }
                ]

                AeroChoice {
                    required property var modelData
                    width: parent.width
                    compact: true
                    selected: root.controller.updatePreference === modelData.key
                    iconSource: "qrc:/assets/icons/" + modelData.icon
                    title: modelData.title
                    detail: modelData.detail
                    onChosen: {
                        root.controller.updatePreference = modelData.key
                        root.controller.goNext()
                    }
                }
            }

            AeroHelpLink {
                objectName: "updateOptionsHelp"
                anchors.left: parent.left
                anchors.leftMargin: 68
                anchors.topMargin: 4
                text: qsTr("Learn more about each option")
                onClicked: updateHelp.open()
            }

            Text {
                anchors.left: parent.left
                anchors.leftMargin: 68
                width: parent.width - 90
                text: qsTr("Updates always require your approval before installation. Change automatic checking in Control Panel > Software Update > Change settings. Setup keeps diagnostic logs locally; review them before sharing.")
                color: "#35424b"
                font.pixelSize: 12
                wrapMode: Text.WordWrap
            }

            AeroHelpLink {
                objectName: "setupPrivacyHelp"
                anchors.left: parent.left
                anchors.leftMargin: 68
                text: qsTr("Read privacy information")
                onClicked: privacyHelp.open()
            }
        }
    ]

    SetupHelpDialog {
        id: updateHelp
        objectName: "updateOptionsDialog"
        title: qsTr("About update settings")
        message: qsTr("Automatic checks contact package repositories while you are signed in and notify you when updates are available. They never install packages or upload diagnostic logs.\n\nOpen Control Panel > Software Update to review and approve a full repository upgrade. Security-only and partial repository upgrades are not supported.\n\nTurn automatic checks on or off in Change settings. Manual checking remains available when automatic checks are off.")
    }

    SetupHelpDialog {
        id: privacyHelp
        objectName: "setupPrivacyDialog"
        title: qsTr("Setup privacy information")
        message: qsTr("Setup and the diagnostic collector write logs locally. The collector does not upload the folder automatically.\n\nDiagnostic logs can include your username, computer name, hardware identifiers, network addresses and file paths. Review the Aero7 Physical Install Logs folder before sharing it; do not post the complete folder publicly without checking its contents.\n\nOnline installation contacts package repositories to download software. Applications and online services you use after installation have their own network activity and privacy practices.")
    }
}
