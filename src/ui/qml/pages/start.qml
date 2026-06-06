import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import RinUI


FluentPage {
    id: startPage

    ColumnLayout {
        Layout.alignment: Qt.AlignCenter
        spacing: 0
        Image {
            // source: "file:///C:\\Users\\Zhang\\Documents\\automatic-video-player\\assets\\images\\logo.png"
            Layout.preferredWidth: 256
            Layout.preferredHeight: 256
            fillMode: Image.PreserveAspectFit
        }

        RowLayout {
            ButtonGroup {
                id: videoTypes
            }
            Layout.alignment: Qt.AlignHCenter
            ToggleButton {
                text: qsTr("News")
                checked: true
                ButtonGroup.group: videoTypes
                onCheckedChanged: {
                    if (checked) {
                        console.log("Switch to News.");
                        AppCentral.video_type_changed("News");
                    }
                }
            }
            ToggleButton {
                text: qsTr("Documentary")
                checked: false
                ButtonGroup.group: videoTypes
                onCheckedChanged: {
                    if (checked) {
                        console.log("Switch to Documentary.");
                        AppCentral.video_type_changed("Documentary");
                    }
                }
            }
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
        Item { Layout.preferredHeight: 100 }
        Button {
            text: qsTr("Normal Play")
            icon.name: "ic_fluent_play_20_regular"
            Layout.alignment: Qt.AlignHCenter
            onClicked: {
                AppCentral.normal_play();
            }
        }
    }
}