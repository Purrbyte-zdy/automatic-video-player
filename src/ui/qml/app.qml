import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import RinUI

FluentWindow {
    id: appWindow
    title: qsTr("Automatic Video Player")
    width: 900
    height: 556
    // icon.name: "ic_fluent_play_20_regular"
    minimumWidth: 500
    minimumHeight: 400
    visible: true


    navigationItems: [
        {
            title: qsTr("Start"),
            icon: "ic_fluent_play_20_regular",
            page: Qt.resolvedUrl("pages/start.qml"),
        },
        {
            title: qsTr("Schedule"),
            icon: "ic_fluent_cube_20_regular",
            page: Qt.resolvedUrl("pages/schedule.qml"),
        },
        {
            title: qsTr("News"),
            icon: "ic_fluent_news_20_regular",
            page: Qt.resolvedUrl("pages/news.qml"),
        },
        {
            title: qsTr("Documentary"),
            icon: "ic_fluent_video_20_regular",
            page: Qt.resolvedUrl("pages/documentary.qml"),
        },
        {
            title: qsTr("Log"),
            icon: "ic_fluent_note_20_regular",
            page: Qt.resolvedUrl("pages/log.qml"),
        },
        {
            title: qsTr("Settings"),
            icon: "ic_fluent_settings_20_regular",
            page: Qt.resolvedUrl("pages/settings.qml"),
        }
    ]

    navigationView.navigationBar.minimumExpandWidth: width + 1
    navigationView.navigationBar.collapsed: true
}