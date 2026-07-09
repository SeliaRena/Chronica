// CyberScrollBar.qml
import QtQuick
import QtQuick.Controls.Basic

ScrollBar {
    id: root

    property color trackColor: "#111318"
    property color thumbColor: "#334155"
    property color thumbHoverColor: "#475569"
    property color thumbPressedColor: "#64748b"

    policy: ScrollBar.AsNeeded
    interactive: true

    implicitWidth: root.orientation === Qt.Vertical ? 14 : 100
    implicitHeight: root.orientation === Qt.Horizontal ? 14 : 100

    background: Rectangle {
        implicitWidth: 14
        implicitHeight: 14
        color: root.trackColor
    }

    contentItem: Rectangle {
        implicitWidth: root.orientation === Qt.Vertical ? 5 : 100
        implicitHeight: root.orientation === Qt.Horizontal ? 5 : 100

        radius: 3

        color: root.pressed
            ? root.thumbPressedColor
            : root.hovered
                ? root.thumbHoverColor
                : root.thumbColor
    }
}