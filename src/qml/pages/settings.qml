import QtQuick
import QtQuick.Layouts
import RinUI

FluentPage {
    Column {
        Layout.fillWidth: true
        spacing: 3
        SettingCard {
            width: parent.width
            icon.name: "ic_fluent_info_20_regular"
            title: qsTr("Copyright Information")
            description: qsTr("Purrbyte-zdy 2026 All rights reserved.\nUsing the AGPL-3.0 license.")
            ToolButton {
                id: githubButton
                icon.name: "ic_fluent_open_20_regular"
                onClicked: {
                    console.log("Settings ToolButton clicked");
                    githubFlyout.open()
                }
            }
        }
        Flyout {
            id: githubFlyout
            parent: githubButton
            text: qsTr("Open This Page: https://github.com/Purrbyte-zdy/automatic-video-player")

            buttonBox: [
                Button {
                    text: qsTr("OK")
                    highlighted: true
                    onClicked: {
                        AppCentral.open_github();
                        githubFlyout.close();
                    }
                }
            ]
        }
    }
}