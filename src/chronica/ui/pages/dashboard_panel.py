from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from src.chronica.ui.styles.style_loader import load_stylesheet

from src.chronica.ui.presentation.models import (
    SessionDisplay, 
    AppUsageInfoDisplay, 
    TopAppsItemData, 
    RecentSessionsItemData
)

from src.chronica.ui.presentation.formatters import (
    simplistic_simplified_ms, 
    ymd_hms
)

from src.chronica.ui.widgets.top_apps_view import TopAppsView
from src.chronica.ui.widgets.recent_sessions_view import RecentSessionsView

from warnings import deprecated

class DashboardPanel(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("dashboardPanel")

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(12, 12, 12, 12)
        root_layout.setSpacing(12)

        self.observation_card = self._build_observation_card()
        self.summary_cards = self._build_summary_cards()
        bottom_row = self._build_bottom_row()

        root_layout.addWidget(self.observation_card)
        root_layout.addWidget(self.summary_cards)
        root_layout.addLayout(bottom_row, 1)
        
        self.setStyleSheet(load_stylesheet("dashboard_panel"))

    def _build_observation_card(self) -> QFrame:
        card = QFrame()
        card.setObjectName("observationCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("Latest Observation")
        title_font = QFont()
        title_font.setPointSize(15)
        title_font.setBold(True)
        title.setFont(title_font)

        grid = QGridLayout()
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(8)

        self.current_app_value = QLabel("Chronica")
        self.current_window_value = QLabel("Dashboard")
        self.last_external_app_value = QLabel("Chrome")
        self.last_external_window_value = QLabel("Personal submissions - Codeforces")
        self.last_observed_duration_value = QLabel("12s")
        self.last_observed_at_value = QLabel("06:00:12")

        self.current_window_value.setWordWrap(True)
        self.last_external_window_value.setWordWrap(True)

        self._add_info_row(grid, 0, "Current App", self.current_app_value)
        self._add_info_row(grid, 1, "Current Window", self.current_window_value)
        self._add_info_row(grid, 2, "Last External App", self.last_external_app_value)
        self._add_info_row(grid, 3, "Last External Window", self.last_external_window_value)
        self._add_info_row(grid, 4, "Last Observed Duration", self.last_observed_duration_value)
        self._add_info_row(grid, 5, "Last Observed At", self.last_observed_at_value)

        layout.addWidget(title)
        layout.addLayout(grid)

        return card

    def _build_summary_cards(self) -> QFrame:
        container = QFrame()
        container.setObjectName("summaryContainer")

        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)

        self.tracked_time_value = QLabel("2m 00s")
        self.sessions_emitted_value = QLabel("17")
        self.unique_apps_value = QLabel("4")
        self.top_app_value = QLabel("Chrome")

        layout.addWidget(self._make_stat_card("Tracked This Cycle", self.tracked_time_value))
        layout.addWidget(self._make_stat_card("Sessions Emitted", self.sessions_emitted_value))
        layout.addWidget(self._make_stat_card("Unique Apps", self.unique_apps_value))
        layout.addWidget(self._make_stat_card("Top App", self.top_app_value))

        return container

    def _build_bottom_row(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(12)

        self.recent_sessions_panel = RecentSessionsView()
        self.top_apps_panel = TopAppsView(item_count=5)

        layout.addWidget(self.recent_sessions_panel, 1)
        layout.addWidget(self.top_apps_panel, 1)

        return layout

    @deprecated("This method is deprecated and will be removed in a future version. Use RecentSessionsView instead.")
    def _build_recent_sessions_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("recentSessionsPanel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("Recent Sessions")
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title.setFont(title_font)

        self.recent_sessions_table = QTableWidget(5, 4)
        self.recent_sessions_table.setObjectName("recentSessionsTable")
        self.recent_sessions_table.setEnabled(False)
        self.recent_sessions_table.setHorizontalHeaderLabels(
            ["Start", "App", "Title", "Duration"]
        )
        
        table_wrapper = QFrame()
        table_wrapper.setObjectName("tableWrapper")
        wrapper_layout = QVBoxLayout(table_wrapper)
        wrapper_layout.setContentsMargins(5, 5, 5, 5)
        wrapper_layout.addWidget(self.recent_sessions_table, 1)

        header = self.recent_sessions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        layout.addWidget(title)
        layout.addWidget(table_wrapper, 1)

        return panel

    @deprecated("This method is deprecated and will be removed in a future version. Use TopAppsView instead.")
    def _build_top_apps_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("topAppsPanel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        title = QLabel("Top Apps")
        title_font = QFont()
        title_font.setPointSize(13)
        title_font.setBold(True)
        title.setFont(title_font)

        self.top_apps_list = QListWidget()
        self.top_apps_list.addItems(
            [
                "Chrome — 1m 41s",
                "Visual Studio Code — 8s",
                "Steam — 8s",
                "Explorer — 3s",
            ]
        )
        
        list_wrapper = QFrame()
        list_wrapper.setObjectName("listWrapper")
        wrapper_layout = QVBoxLayout(list_wrapper)
        wrapper_layout.setContentsMargins(5, 5, 5, 5)
        wrapper_layout.addWidget(self.top_apps_list, 1)

        layout.addWidget(title)
        layout.addWidget(list_wrapper, 1)

        return panel

    def _make_stat_card(self, label_text: str, value_label: QLabel) -> QFrame:
        card = QFrame()
        card.setObjectName("statCard")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(14, 12, 14, 12)
        layout.setSpacing(4)

        label = QLabel(label_text)
        label_font = QFont()
        label_font.setItalic(True)
        label.setFont(label_font)

        value_font = QFont()
        value_font.setPointSize(14)
        value_font.setBold(True)
        value_label.setFont(value_font)

        layout.addWidget(label)
        layout.addWidget(value_label)

        return card

    def _add_info_row(self, layout: QGridLayout, row: int, key: str, value: QLabel) -> None:
        key_label = QLabel(f"{key}:")
        key_font = QFont()
        key_font.setBold(True)
        key_label.setFont(key_font)

        layout.addWidget(key_label, row, 0, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(value, row, 1)

    def refresh_recent_sessions(self, recent_sessions: tuple[RecentSessionsItemData, ...]) -> None:
        self.recent_sessions_panel.set_recent_sessions(recent_sessions)
                    
    def refresh_top_apps(self, top_apps: tuple[TopAppsItemData, ...]) -> None:
        self.top_apps_panel.set_items_data(top_apps)

    def set_current_app(self, text: str) -> None:
        self.current_app_value.setText(text)

    def set_current_window(self, text: str) -> None:
        self.current_window_value.setText(text)

    def set_last_external_app(self, text: str) -> None:
        self.last_external_app_value.setText(text)

    def set_last_external_window(self, text: str) -> None:
        self.last_external_window_value.setText(text)

    def set_last_observed_duration(self, text: str) -> None:
        self.last_observed_duration_value.setText(text)

    def set_last_observed_at(self, text: str) -> None:
        self.last_observed_at_value.setText(text)

    def set_tracked_time(self, text: str) -> None:
        self.tracked_time_value.setText(text)

    def set_sessions_emitted(self, text: str) -> None:
        self.sessions_emitted_value.setText(text)

    def set_unique_apps(self, text: str) -> None:
        self.unique_apps_value.setText(text)

    def set_top_app(self, text: str) -> None:
        self.top_app_value.setText(text)