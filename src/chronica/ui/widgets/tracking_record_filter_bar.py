from PySide6.QtCore import Signal, QSize, Qt
from PySide6.QtGui import QIcon, QFont
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QLabel,
    QComboBox,
    QLineEdit,
    QPushButton,
    QToolButton,
    QMenu,
    QWidgetAction
)

from src.chronica.storage.sqlite.query import (
    TrackingRecordTimeFilter,
    TrackingRecordDurationFilter,
    TrackingRecordSortMode,
    TrackingRecordQuery
)

from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.common.resource_locator import ResourceLocator

class TrackingRecordFilterBar(QFrame):
    query_applied = Signal(TrackingRecordQuery)
    
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("trackingRecordFilterBar")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(2)
        
        self.search_input = QLineEdit()
        self.search_input.setObjectName("searchInput")
        self.search_input.setPlaceholderText("Search by title...")
        
        self.time_filter_combo = QComboBox()
        self.time_filter_combo.setObjectName("timeFilterCombo")
        self.time_filter_combo.addItem("All", TrackingRecordTimeFilter.ALL)
        self.time_filter_combo.addItem("Today", TrackingRecordTimeFilter.TODAY)
        self.time_filter_combo.addItem("Last 24 hours", TrackingRecordTimeFilter.LAST_24_HOURS)
        self.time_filter_combo.addItem("Last 7 days", TrackingRecordTimeFilter.LAST_7_DAYS)
        self.time_filter_combo.addItem("Last 30 days", TrackingRecordTimeFilter.LAST_30_DAYS)
        
        self.duration_filter_combo = QComboBox()
        self.duration_filter_combo.setObjectName("durationFilterCombo")
        self.duration_filter_combo.addItem("All", TrackingRecordDurationFilter.ALL)
        self.duration_filter_combo.addItem("< 5 minutes", TrackingRecordDurationFilter.LESS_THAN_5_MINUTES)
        self.duration_filter_combo.addItem("< 1 hour", TrackingRecordDurationFilter.LESS_THAN_1_HOUR)
        self.duration_filter_combo.addItem("< half day", TrackingRecordDurationFilter.LESS_THAN_HALF_DAY)
        self.duration_filter_combo.addItem("< 1 day", TrackingRecordDurationFilter.LESS_THAN_1_DAY)
        self.duration_filter_combo.addItem(">= 1 day", TrackingRecordDurationFilter.MORE_OR_EQUAL_THAN_1_DAY)
        
        self.sort_mode_combo = QComboBox()
        self.sort_mode_combo.setObjectName("sortModeCombo")
        self.sort_mode_combo.addItem("Title A-Z", TrackingRecordSortMode.TITLE_ASC)
        self.sort_mode_combo.addItem("Title Z-A", TrackingRecordSortMode.TITLE_DESC)
        self.sort_mode_combo.addItem("Newest", TrackingRecordSortMode.NEWEST_FIRST)
        self.sort_mode_combo.addItem("Oldest", TrackingRecordSortMode.OLDEST_FIRST)
        self.sort_mode_combo.addItem("Longest duration", TrackingRecordSortMode.LONGEST_DURATION_FIRST)
        self.sort_mode_combo.addItem("Shortest duration", TrackingRecordSortMode.SHORTEST_DURATION_FIRST)
        
        self.send_query_button = QPushButton("Apply")
        self.send_query_button.setObjectName("sendQueryButton")
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setObjectName("resetButton")
        
        self.filter_tool_open_button = QToolButton()
        self.filter_tool_open_button.setObjectName("filterToolOpenButton")
        self.filter_tool_open_button.setIcon(QIcon(str(ResourceLocator.ui_icon("blue filter.png"))))
        self.filter_tool_open_button.setIconSize(QSize(20, 20))
        self.filter_tool_open_button.setText("Filter Options")
        self.filter_tool_open_button.setToolTip("Open to filter tracking records with more options.")
        self.filter_tool_open_button.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        
        self.filter_menu = QMenu(self.filter_tool_open_button)
        filter_options_popup = self._build_filter_options_popup()
        
        filter_popup_action = QWidgetAction(self.filter_menu)
        filter_popup_action.setDefaultWidget(filter_options_popup)
        
        self.filter_menu.addAction(filter_popup_action)
        self.filter_tool_open_button.setMenu(self.filter_menu)
        
        layout.addWidget(self.search_input)
        layout.addWidget(self.filter_tool_open_button)
        
        self._connect_internal_signals()
        self.setStyleSheet(load_stylesheet("tracking_record_filter_bar"))

    def make_query(self) -> TrackingRecordQuery:
        return TrackingRecordQuery(
            time_filter=self.time_filter_combo.currentData(),
            duration_filter=self.duration_filter_combo.currentData(),
            search_text=self.search_input.text(),
            sort_mode=self.sort_mode_combo.currentData()
        )
        
    def _build_filter_options_popup(self) -> QWidget:
        popup = QWidget()
        popup.setObjectName("filterOptionsPopup")
        popup_layout = QHBoxLayout(popup)
        popup_layout.setContentsMargins(10, 10, 10, 10)
        popup_layout.setSpacing(12)
        
        common_label_font = QFont()
        common_label_font.setPointSize(8)
        
        time_filter_label = QLabel("Time Filters:")
        time_filter_label.setFont(common_label_font)
        duration_filter_label = QLabel("Duration Filters:")
        duration_filter_label.setFont(common_label_font)
        sort_mode_label = QLabel("Sort Mode:")
        sort_mode_label.setFont(common_label_font)
        
        combos = QWidget()
        combos.setObjectName("popupCombos")
        combos_layout = QVBoxLayout(combos)
        combos_layout.setContentsMargins(12, 12, 12, 12)
        combos_layout.addWidget(time_filter_label)
        combos_layout.addWidget(self.time_filter_combo)
        combos_layout.addWidget(duration_filter_label)
        combos_layout.addWidget(self.duration_filter_combo)
        combos_layout.addWidget(sort_mode_label)
        combos_layout.addWidget(self.sort_mode_combo)
        
        buttons = QWidget()
        buttons.setObjectName("popupButtons")
        buttons_layout = QVBoxLayout(buttons)
        buttons_layout.setContentsMargins(12, 12, 12, 12)
        buttons_layout.addWidget(self.send_query_button, alignment=Qt.AlignmentFlag.AlignBottom)
        buttons_layout.addWidget(self.reset_button, alignment=Qt.AlignmentFlag.AlignTop)
        
        popup_layout.addWidget(combos)
        popup_layout.addWidget(buttons)
        
        return popup

    def _connect_internal_signals(self) -> None:
        self.send_query_button.clicked.connect(self._on_send_query_button_clicked)
        self.reset_button.clicked.connect(self._on_reset_button_clicked)
        
    def _on_send_query_button_clicked(self) -> None:
        self.query_applied.emit(self.make_query())
        
    def _on_reset_button_clicked(self) -> None:
        self.search_input.setText("")
        self.search_input.setPlaceholderText("Search by title...")
        
        self.time_filter_combo.setCurrentIndex(0)
        self.duration_filter_combo.setCurrentIndex(0)
        self.sort_mode_combo.setCurrentIndex(0)