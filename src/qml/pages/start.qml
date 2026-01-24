import QtQuick
import QtQuick.Controls
import QtQuick.Window
import RinUI


FluentPage {
    id: startPage

    PillButton {
        text: qsTr("Force Play")
        icon.name: "ic_fluent_approvals_app_20_regular"
        checked: true
        checkable: false
        onClicked: {
            AppCentral.force_play();
        }
    }
}