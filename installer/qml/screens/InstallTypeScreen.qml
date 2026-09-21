import QtQuick
import "../components"

SetupPage {
    id: root
    anchors.fill: parent
    title: qsTr("Which type of installation do you want?")
    description: ""
    showBack: true
    showNext: false
    showFooter: false

    body: [
        Column {
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            spacing: 8

            AeroChoice {
                width: parent.width
                height: 108
                enabled: false
                iconSource: "qrc:/assets/icons/install-alongside.svg"
                title: qsTr("Upgrade")
                detail: qsTr("Upgrade an existing Aero7 installation and keep files and settings. This option is not available when setup is started from the installation media.")
            }

            AeroChoice {
                width: parent.width
                height: 112
                selected: root.controller.installType === "erase"
                iconSource: "qrc:/assets/icons/install-clean.svg"
                title: qsTr("Custom (advanced)")
                detail: qsTr("Install a new copy of Aero7. You can erase a complete disk, use unallocated space, format one selected partition, or shrink an NTFS Windows partition after opening Drive options (advanced).")
                onChosen: {
                    root.controller.installType = "erase"
                    root.controller.goNext()
                }
            }

            AeroHelpLink {
                objectName: "installTypeHelp"
                anchors.left: parent.left
                anchors.leftMargin: 80
                text: qsTr("Help me decide")
                onClicked: installHelp.open()
            }
        }
    ]

    SetupHelpDialog {
        id: installHelp
        objectName: "installTypeDialog"
        title: qsTr("Choosing an installation type")
        message: qsTr("Choose Custom to install a new copy of Aero7. Erasing a complete disk deletes its existing partitions and files. Back up important data first.\n\nDrive options (advanced) offers supported free-space, partition-format and NTFS-shrink choices. Verify the selected disk and the final confirmation carefully; selecting Custom alone does not erase a disk.\n\nIn-place Upgrade is not available from this installation media.")
    }
}
