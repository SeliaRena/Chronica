from __future__ import annotations

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)

from src.chronica.ui.styles.style_loader import load_stylesheet
from src.chronica.ui.resources import (
    QIcons,
    Stylesheets
)

from src.chronica.ui.presentation.models import (
    TopAppsItemData,
    RecentSessionsItemData
)

from src.chronica.ui.widgets.common import (
    PlainIconHeader,
    VMetricCard
)

from src.chronica.ui.widgets.common.factories import (
    container
)

from src.chronica.ui.widgets.top_apps_view import TopAppsView
from src.chronica.ui.widgets.recent_sessions_view import RecentSessionsView

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
        
        self.setStyleSheet(Stylesheets.load("dashboard_panel.qss"))

    def _build_observation_card(self) -> QFrame:
        card, card_layout = container(
            host=QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="observationCard",
            vertical=True,
            margins=(16, 16, 16, 16),
            spacing=12
        )
        
        card_header = PlainIconHeader(
            icon=QIcons.get("bar-chart.png"),
            title="Latest Observation",
            icon_w=24,
            icon_h=24,
            title_px=18,
        )
        
        card_content, content_layout = container(
            host=QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="observationCardContent",
            vertical=False,
            margins=(0, 0, 0, 0),
            spacing=6
        )
        
        accent_bar = QFrame(frameShape=QFrame.Shape.NoFrame)
        accent_bar.setObjectName("observationCardAccentBar")
        accent_bar.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        accent_bar2 = QFrame(frameShape=QFrame.Shape.NoFrame)
        accent_bar2.setObjectName("observationCardAccentBar2")
        accent_bar2.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        
        stat_titles, titles_layout = container(
            host=QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="observationCardStatTitles",
            vertical=True,
            margins=(6, 5, 0, 5),
            spacing=5
        )
        
        titles_layout.addWidget(QLabel("Current App:"))
        titles_layout.addWidget(QLabel("Current Window:"))
        titles_layout.addWidget(QLabel("Last External App:"))
        titles_layout.addWidget(QLabel("Last External Window:"))
        titles_layout.addWidget(QLabel("Last Observed Duration:"))
        titles_layout.addWidget(QLabel("Last Observed At:"))
        
        stat_values, values_layout = container(
            host=QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="observationCardStatValues",
            vertical=True,
            margins=(6, 5, 0, 5),
            spacing=5
        )
        
        self.current_app_value = QLabel("Chronica")
        self.current_window_value = QLabel("Dashboard")
        self.last_external_app_value = QLabel("Chrome")
        self.last_external_window_value = QLabel("Personal submissions - Codeforces")
        self.last_observed_duration_value = QLabel("12s")
        self.last_observed_at_value = QLabel("06:00:12")
        
        values_layout.addWidget(self.current_app_value)
        values_layout.addWidget(self.current_window_value)
        values_layout.addWidget(self.last_external_app_value)
        values_layout.addWidget(self.last_external_window_value)
        values_layout.addWidget(self.last_observed_duration_value)
        values_layout.addWidget(self.last_observed_at_value)
        
        content_layout.addWidget(accent_bar)
        content_layout.addWidget(stat_titles)
        content_layout.addWidget(accent_bar2)
        content_layout.addWidget(stat_values)
        
        card_layout.addWidget(card_header)
        card_layout.addWidget(card_content)
        
        return card

    def _build_summary_cards(self) -> QFrame:
        summary_cards, summary_layout = container(
            host=QFrame(frameShape=QFrame.Shape.NoFrame),
            host_object_name="summaryCards",
            vertical=False,
            margins=(0, 0, 0, 0),
            spacing=12
        )

        self.tracked_time_card = self._make_dashboard_metric_card("Tracked Time", "20m 35s")
        self.sessions_emitted_card = self._make_dashboard_metric_card("Sessions Emitted", "15")
        self.unique_apps_card = self._make_dashboard_metric_card("Unique Apps", "7")
        self.top_app_card = self._make_dashboard_metric_card("Top App", "Chrome")

        summary_layout.addWidget(self.tracked_time_card)
        summary_layout.addWidget(self.sessions_emitted_card)
        summary_layout.addWidget(self.unique_apps_card)
        summary_layout.addWidget(self.top_app_card)

        return summary_cards
    
    def _make_dashboard_metric_card(self, label_text: str, value_text: str) -> VMetricCard:
        return VMetricCard(
            title=label_text,
            value=value_text,
            value_font_weight=400,
            value_font_family="Sora",
            value_font_px=18,
            border=False,
        )

    def _build_bottom_row(self) -> QHBoxLayout:
        layout = QHBoxLayout()
        layout.setSpacing(12)

        self.recent_sessions_panel = RecentSessionsView()
        self.top_apps_panel = TopAppsView(item_count=5)

        layout.addWidget(self.recent_sessions_panel, 1)
        layout.addWidget(self.top_apps_panel, 1)

        return layout

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
        self.tracked_time_card.set_value(text)

    def set_sessions_emitted(self, text: str) -> None:
        self.sessions_emitted_card.set_value(text)

    def set_unique_apps(self, text: str) -> None:
        self.unique_apps_card.set_value(text)

    def set_top_app(self, text: str) -> None:
        self.top_app_card.set_value(text)