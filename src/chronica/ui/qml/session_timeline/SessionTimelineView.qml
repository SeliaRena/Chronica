import QtQuick
import QtQuick.Controls
import "../components"

pragma ComponentBehavior: Bound

// Root session timeline component.
//
// Consumes timelineBridge.model (QVariantMap) shaped as QmlData.to_view_dict():
//   { visibleStartTsMs, visibleEndTsMs, axisTicks[], rows[] }
//
// Three visual areas:
//   Axis area   — sticky top:  scrolls H with timeline, never moves vertically.
//   Label area  — sticky left: scrolls V with timeline, never moves horizontally.
//   Timeline    — scrollable both H and V.
//
// Scale: 1 s = 1 px. drawX, drawWidth, and axisTick.realX are in this space.
Item {
    id: root

    // --- Layout constants ---
    readonly property int labelWidth:      root.width * 0.2
    readonly property int labelGap:        7
    readonly property int rowHeight:       42
    readonly property int rowGap:          8
    readonly property int topPadding:      42 // axis strip height
    readonly property int bottomPadding:   32
    readonly property int rowStartPadding: 24 // left margin inside timeline content
    readonly property int axisGap:          5 // extra space between axis ticks and timeline area

    // --- Model interface ---
    property var model: timelineBridge.model

    // --- Values derived from model ---
    readonly property real _visibleStartMs: (model && model.visibleStartTsMs) ? model.visibleStartTsMs : 0
    readonly property real _visibleEndMs:   (model && model.visibleEndTsMs)   ? model.visibleEndTsMs   : 0
    readonly property var  _rows:           (model && model.rows)             ? model.rows             : []
    readonly property var  _axisTicks:      (model && model.axisTicks)        ? model.axisTicks        : []

    // Timeline content width in pixels (1 s = 1 px)
    readonly property real timelineWidth: Math.max(900, (_visibleEndMs - _visibleStartMs) / 1000)

    // --- Derived layout ---
    readonly property real _rowsBlockHeight: _rows.length * (root.rowHeight + root.rowGap)
    // Height available to timeline rows (below the sticky axis strip)
    readonly property real _flickableHeight: innerContent.height - root.topPadding - root.axisGap
    // Vertical start for rows: centred when they fit, otherwise flush to top
    readonly property real _rowsStartY:     Math.max(0, (_flickableHeight - _rowsBlockHeight) / 2)
    readonly property real _contentHeight:  Math.max(_flickableHeight, _rowsStartY + _rowsBlockHeight + root.bottomPadding)

    // --- Root background ---
    Rectangle {
        anchors.fill: parent
        color: "#0a0a0a"
    }

    // --- Inner content with 7 px margins ---
    Item {
        id: innerContent
        anchors.fill:    parent
        anchors.margins: 7

        // ── Right panel: axis strip (sticky top) + timeline Flickable ──────
        // Single rounded rectangle that clips both areas consistently.
        Rectangle {
            id:     rightPanel
            x:      root.labelWidth + root.labelGap
            y:      0
            width:  parent.width - root.labelWidth - root.labelGap
            height: parent.height
            color:  "#0a0a0a"
            radius: 5
            clip:   true

            // Axis strip — fixed at top, follows horizontal scroll only
            Item {
                id:     axisArea
                x:      0
                y:      0
                z:      30
                width:  parent.width
                height: root.topPadding

                SessionTimelineAxis {
                    // Track horizontal scroll so ticks stay aligned with segments
                    x:      root.rowStartPadding - flickable.contentX
                    y:      0
                    z:      30
                    width:  root.timelineWidth
                    height: root.topPadding
                    ticks:  root._axisTicks
                }

                // axisArea background: covers the top of the timeline Flickable so it doesn't show through
                Rectangle {
                    x:      0
                    y:      0
                    z:      29
                    width:  parent.width
                    height: root.topPadding
                    color:  "#111111"
                    radius: 5
                }
            }

            Rectangle {
                id:     timelineAreaBackground
                x:      0
                y:      root.topPadding + root.axisGap
                width:  parent.width
                height: parent.height - root.topPadding - root.axisGap
                radius: 5
                clip:   true

                gradient: Gradient {
                    orientation: Gradient.Vertical

                    GradientStop { position: 0.0; color: "#24262a" }
                    GradientStop { position: 0.55; color: "#202328" }
                    GradientStop { position: 1.0; color: "#1b1f26" }
                }

                // Timeline rows — scrollable H and V
                Flickable {
                    id:     flickable
                    x:      0
                    y:      0
                    width:  parent.width
                    height: parent.height

                    contentWidth:  root.timelineWidth + root.rowStartPadding + 80
                    contentHeight: root._contentHeight

                    flickableDirection: Flickable.HorizontalAndVerticalFlick

                    ScrollBar.horizontal: CyberScrollBar { policy: ScrollBar.AsNeeded }
                    ScrollBar.vertical:   CyberScrollBar { policy: ScrollBar.AsNeeded }

                    Repeater {
                        id:    rowRepeater
                        model: root._rows

                        delegate: SessionTimelineRow {
                            required property var modelData
                            required property int index

                            x:      root.rowStartPadding
                            y:      root._rowsStartY + index * (root.rowHeight + root.rowGap)
                            width:  root.timelineWidth
                            height: root.rowHeight

                            rowData:       modelData
                            segmentHeight: 22
                        }
                    }
                }
            }
        }

        // ── Label panel: sticky left, scrolls vertically with the Flickable ─
        Rectangle {
            id:     labelPanel
            x:      0
            y:      root.topPadding + root.axisGap
            width:  root.labelWidth
            height: parent.height - root.topPadding - root.axisGap
            color:  "#111111"
            radius: 5
            clip:   true
            z:      10

            // Inner clip area keeps labels away from the rounded border edges
            Item {
                x:      5
                y:      5
                width:  parent.width - 10
                height: parent.height - 10
                clip:   true

                // Tracks vertical scroll; -5 compensates for clip-inner y offset
                Item {
                    y:      root._rowsStartY - flickable.contentY - 5
                    width:  parent.width
                    height: root._rowsBlockHeight

                    Repeater {
                        model: root._rows

                        delegate: Rectangle {
                            required property var modelData
                            required property int index

                            x:      0
                            y:      index * (root.rowHeight + root.rowGap)
                            width:  parent.width
                            height: root.rowHeight
                            radius: 5

                            gradient: Gradient {
                                orientation: Gradient.Horizontal

                                GradientStop { position: 0.0;  color: "#261B3F" }
                                GradientStop { position: 0.55; color: "#181D28" }
                                GradientStop { position: 1.0;  color: "#1B202B" }
                            }

                            Text {
                                x:              11
                                y:              (parent.height - height) / 2
                                text:           parent.modelData.label
                                color:          "#ddddce"
                                font.pixelSize: 12
                                font.family:    "Segoe UI"
                                font.bold:      true
                                elide:          Text.ElideRight
                                width:          parent.width - 16
                            }
                        }
                    }
                }
            }
        }

        // ── Corner piece: covers the label/axis intersection ───────────────
        Rectangle {
            x:      0
            y:      0
            z:      30
            width:  root.labelWidth
            height: root.topPadding
            color:  "#111111"
            radius: 5
        }
    }
}
