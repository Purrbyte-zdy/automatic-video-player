import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import RinUI

FluentPage {
    id: schedulePage
    property int nowTimeline : 1
    ColumnLayout {
        Button {
            id: newTimeline
            text: qsTr("New Timeline")
            icon.name: "ic_fluent_timeline_20_regular"
            onClicked: {
                AppCentral.new_timeline();
                schedulePage.nowTimeline ++;
            }
        }
        Text {
            id: timelineName
            text: qsTr("Timeline %1").arg(schedulePage.nowTimeline)
        }
        // Day
    }
}