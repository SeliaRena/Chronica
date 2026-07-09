import QtQuick
import QtQuick.Controls

pragma ComponentBehavior: Bound

// One timeline repeater item — either a normal session bar or a clustered
// group of tiny sessions. Receives a QmlRepeaterItem dict:
//
//   kind:         "normal" | "clustered"
//   drawX:        float   – x position in pixels (1 s = 1 px, relative to visible start)
//   drawWidth:    float   – rendered width in pixels
//   hitTestWidth: float   – ignored (same as drawWidth)
//   segments:     QmlSegment[]
//     realX, realWidth, color, tiny, tooltip
//     session: { appName, appPath, windowTitle, startTsMs, endTsMs,
//                startDtText, endDtText, durationMs, durationText, timezoneInfo }
//   tooltip: str
//
// Normal items have exactly one segment. Clustered items contain several tiny
// ones, already grouped by the backend — no clustering logic belongs here.
Item {
    id: root

    property var itemData:      null
    property int rowHeight:     42
    property int segmentHeight: 20

    readonly property bool _isNormal:    itemData !== null && itemData.kind === "normal"
    readonly property bool _isClustered: itemData !== null && itemData.kind === "clustered"
    readonly property var  _seg0:        (_isNormal && itemData.segments && itemData.segments.length > 0)
                                         ? itemData.segments[0] : null

    x:      itemData ? itemData.drawX : 0
    y:      (rowHeight - segmentHeight) / 2
    width:  itemData ? Math.max(1, itemData.drawWidth) : 0
    height: segmentHeight

    // Clustered items sit above normal items within the same row.
    z: _isClustered ? 20 : 10

    // ── Normal segment ─────────────────────────────────────────────────────

    // Coloured bar
    Rectangle {
        visible:      root._isNormal
        anchors.fill: parent
        radius:       2

        color:        root._seg0 ? root._seg0.color : "#4CC9F0"
        // Normal items are slightly transparent so underlying tracks remain
        // readable when rows overlap due to zooming.
        opacity:      hoverArea.containsMouse ? 1.0 : 0.88

        border.color: hoverArea.containsMouse ? "#FFFFFF" : "transparent"
        border.width: hoverArea.containsMouse ? 1.5 : 0.0

        Behavior on opacity      { NumberAnimation { duration: 100 } }
        Behavior on border.width { NumberAnimation { duration: 100 } }
    }

    // Window title label — top-left anchored, elides when the bar is too narrow.
    Text {
        visible:              root._isNormal
        text:                 root._seg0 ? root._seg0.session.windowTitle : ""
        color:                "#FFFFFF"
        opacity:              0.85
        font.pixelSize:       10
        elide:                Text.ElideRight
        anchors.top:          parent.top
        anchors.left:         parent.left
        anchors.topMargin:    2
        anchors.leftMargin:   3
        width:                parent.width - 6
    }

    // ── Clustered segment ──────────────────────────────────────────────────

    // Dark background makes the cluster visually distinct from normal bars.
    Rectangle {
        visible:      root._isClustered
        anchors.fill: parent
        radius:       2
        color:        "#1A2438"
        // Slightly higher opacity than normal so the cluster reads as "more
        // important" (higher z) without obscuring normal items completely.
        opacity:      hoverArea.containsMouse ? 0.95 : 0.82
    }

    // Individual segment strips rendered at their real positions within the
    // cluster's draw bounds. realX is absolute; subtract drawX for local coords.
    Repeater {
        model: root._isClustered && root.itemData ? root.itemData.segments : null

        delegate: Rectangle {
            required property var modelData

            x:       modelData.realX - root.itemData.drawX
            y:       0
            width:   Math.max(1, modelData.realWidth)
            height:  root.segmentHeight
            radius:  1
            color:   modelData.color
            opacity: hoverArea.containsMouse ? 0.95 : 0.80
        }
    }

    // ── Hover and tooltip ─────────────────────────────────────────────────

    MouseArea {
        id:           hoverArea
        anchors.fill: parent
        hoverEnabled: true
        cursorShape:  Qt.PointingHandCursor

        ToolTip {
            visible: hoverArea.containsMouse && root.itemData !== null
            delay:   400
            text:    root.itemData ? root.itemData.tooltip : ""
        }
    }
}
