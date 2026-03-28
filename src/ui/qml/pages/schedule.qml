import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import RinUI

FluentPage {
    id: schedulePage
    property int nowTimeline : 1
    ColumnLayout {
        RowLayout {
            Text {
                id: timelineName
                text: qsTr("Timeline %1").arg(schedulePage.nowTimeline)
                Layout.alignment: Qt.AlignLeft
            }

            Item { Layout.fillWidth: true } // spacer pushes button to the right

            Button {
                id: newTimeline
                text: qsTr("New Timeline")
                icon.name: "ic_fluent_timeline_20_regular"
                onClicked: {
                    AppCentral.new_timeline();
                    schedulePage.nowTimeline ++;
                }
            }
        }

        RowLayout {
            Text {
                text: qsTr("Playback Time")
                Layout.alignment: Qt.AlignLeft
            }

            Item { Layout.fillWidth: true }

            TimePicker {
                id: playbackTimePicker
                use24Hour: true
                onTimeChanged: {
                    AppCentral.set_time(hour, minute, 0);
                }
            }
        }

        RowLayout {
            Text {
                text: qsTr("End Time")
                Layout.alignment: Qt.AlignLeft
            }

            Item { Layout.fillWidth: true }

            TimePicker {
                id: endTimePicker
                use24Hour: true
                onTimeChanged: {
                    AppCentral.set_time(hour, minute, 1);
                }
            }
        }
    }
}
