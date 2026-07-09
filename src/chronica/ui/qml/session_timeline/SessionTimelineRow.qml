import QtQuick

// One row in the session timeline: a horizontal guide line and a list of
// repeater items (normal or clustered segments).
//
// rowData = { label: str, repeaterItems: QmlRepeaterItem[] }
// The label is rendered in the sticky panel inside SessionTimelineView.
// Each repeater item carries pre-computed drawX / drawWidth — no scaling needed.
Item {
    id: root

    property var rowData:       null
    property int segmentHeight: 20

    // Row guide line spanning the full track width
    Rectangle {
        x:      0
        y:      root.height / 2
        width:  parent.width
        height: 1
        color:  "#323232"
    }

    // Repeater items — normal sessions and clustered groups of tiny sessions
    Repeater {
        model: root.rowData ? root.rowData.repeaterItems : null

        delegate: SessionTimelineSegment {
            required property var modelData

            itemData:      modelData
            rowHeight:     root.height
            segmentHeight: root.segmentHeight
        }
    }
}