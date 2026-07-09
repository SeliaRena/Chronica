import QtQuick

// Horizontal time axis driven entirely by pre-computed backend data.
//
// Receives model.axisTicks[], each shaped as:
//   { realX: float, timestampMs: int, label: str, kind: "minor"|"day_boundary" }
//
// realX is already in 1 s = 1 px coordinates — do not recompute.
// label is already formatted timezone-aware — do not reformat with JS Date.
// Day-boundary ticks get a full-height rule and a brighter label.
Item {
    id: root

    property var ticks: []

    // Axis baseline rule
    Rectangle {
        x:      0
        y:      parent.height - 7
        width:  parent.width
        height: 1
        color:  "#8a8a8d"
    }

    Repeater {
        model: root.ticks

        delegate: Item {
            required property var modelData
            required property int index

            readonly property bool isDayBoundary: modelData.kind === "day_boundary"

            // Centre the 36px-wide item on realX so the tick mark lands exactly there.
            x:      modelData.realX - 18
            y:      0
            width:  36
            height: root.height

            // Day-boundary: full-height vertical rule
            Rectangle {
                visible: parent.isDayBoundary
                x:       18
                y:       0
                width:   1
                height:  parent.height
                color:   "#6B7A99"
            }

            // Minor tick: small notch at the baseline
            Rectangle {
                visible: !parent.isDayBoundary
                x:       18
                y:       parent.height - 10 - 7
                width:   1
                height:  10
                color:   "#8a8a8d"
            }

            // Label
            Text {
                text:                     parent.modelData.label
                color:                    parent.isDayBoundary ? "#A8B4CC" : "#8a8a8d"
                font.pixelSize:           parent.isDayBoundary ? 10 : 9
                font.bold:                parent.isDayBoundary
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top:              parent.top
                anchors.topMargin:        5
            }
        }
    }
}
