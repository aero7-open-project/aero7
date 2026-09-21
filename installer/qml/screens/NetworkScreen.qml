pragma ComponentBehavior: Bound
import QtQuick
import "../components"

SetupPage {
    id: root
    anchors.fill: parent
    title: qsTr("Select your computer's current location")
    description: qsTr("Aero7 will apply firewall settings to this network. File sharing must be configured separately.")
    showBack: true
    showNext: false
    showFooter: false

    body: [
        Column {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            spacing: 3

            Repeater {
                model: [
                    { key: "home", icon: "network-home.svg", title: qsTr("Home network"), detail: qsTr("For a trusted home network. Permits local device discovery; file sharing and remote access stay off.") },
                    { key: "work", icon: "network-work.svg", title: qsTr("Work network"), detail: qsTr("For your workplace. Blocks unsolicited connections until you allow the services your organization needs.") },
                    { key: "public", icon: "network-public.svg", title: qsTr("Public network"), detail: qsTr("For cafés, airports, mobile broadband, and other networks you do not fully trust.") }
                ]

                AeroChoice {
                    required property var modelData
                    width: parent.width
                    compact: true
                    selected: root.controller.networkChoice === modelData.key
                    iconSource: "qrc:/assets/icons/" + modelData.icon
                    title: modelData.title
                    detail: modelData.detail
                    onChosen: {
                        root.controller.networkChoice = modelData.key
                        root.controller.goNext()
                    }
                }
            }

            Text {
                anchors.left: parent.left
                anchors.leftMargin: 68
                anchors.right: parent.right
                wrapMode: Text.WordWrap
                text: qsTr("If you aren't sure, select Public. When no single connected network can be identified, Public defaults stay in place. You can change a connected network's location later in Control Panel > Firewall.")
                color: "#4e5961"
                font.pixelSize: 12
            }
        }
    ]
}
