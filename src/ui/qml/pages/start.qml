import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import RinUI


ColumnLayout {
    // Background image: cover the entire page, scale with window, semi-transparent
    Image {
        id: backgroundImage
        anchors.fill: parent
        fillMode: Image.PreserveAspectCrop
        opacity: 0.5
        Component.onCompleted: {
            if (typeof PathManager !== 'undefined' && PathManager !== null) {
                backgroundImage.source = PathManager.images("logo.png")
            } else {
                // fallback: relative asset path (adjust if needed)
                backgroundImage.source = "assets/images/logo.png"
            }
        }
    }
    // keep the ButtonGroup in case other logic refers to it
    ButtonGroup {
        id: videoTypesColumnLayout
    }

    // PillButton placed at the bottom center of the page with 10px margin
    PillButton {
        id: forcePlayButton
        text: qsTr("Force Play")
        icon.name: "ic_fluent_approvals_app_20_regular"
        checked: true
        checkable: false
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 10
        onClicked: {
            AppCentral.force_play();
        }
    }
}