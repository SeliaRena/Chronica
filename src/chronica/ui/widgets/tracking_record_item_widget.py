from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QSizePolicy,
    QMessageBox
)

from PySide6.QtCore import Qt, Signal, Slot

from src.chronica.ui.resources import (
    Stylesheets,
    QIcons
)

from src.chronica.ui.presentation.formatters import (
    simplistic_simplified_ms,
    ymd_hms,
    human_readable
)

from src.chronica.ui.widgets.common import (
    PlainIconHeader
)

from src.chronica.ui.widgets.common.factories import (
    icon_button
)

from src.chronica.ui.presentation.models import TrackingRecordDisplay

from src.chronica.characters.character import Character
from src.chronica.characters.dialogues import Scenario
from src.chronica.characters.models import DialogueRenderContext
from src.chronica.characters.builders import DialogueRenderContextBuilder

class TrackingRecordItemWidget(QFrame):
    explain_record_requested = Signal(object)
    delete_record_requested = Signal(str, object)
    
    def __init__(
        self,
        record: TrackingRecordDisplay,
        character: Character,
        parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        self.setObjectName("trackingRecordItemWidget")
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.chronica = character
        self.record = record

        self.header = PlainIconHeader(
            QIcons.get("order-history.png"),
            record.title,
            icon_w=24,
            icon_h=24,
            title_px=12,
            compress_content_left=False,
        )
        
        # start / end time labels
        self.time_labels = QFrame(frameShape=QFrame.Shape.NoFrame)
        time_layout = QVBoxLayout(self.time_labels)
        time_layout.setContentsMargins(0, 0, 0, 0)
        time_layout.setSpacing(5)
        
        self.start_time_label = QLabel(ymd_hms(record.start))
        self.start_time_label.setObjectName("recordItemStartTimeLabel")
        self.end_time_label = QLabel(f"➝ {ymd_hms(record.end)}")
        self.end_time_label.setObjectName("recordItemEndTimeLabel")
        
        time_layout.addWidget(self.start_time_label)
        time_layout.addWidget(self.end_time_label)
        
        # icon buttons
        self.icon_buttons = QFrame(frameShape=QFrame.Shape.NoFrame)
        buttons_layout = QHBoxLayout(self.icon_buttons)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(5)
        
        self.edit_button = icon_button(
            QIcons.get("file-edit.svg"),
            button_size=20,
            icon_size=16,
            object_name="recordItemEditButton",
            tooltip="Edit attributes of this record"
        )
        
        self.info_button = icon_button(
            QIcons.get("info.svg"),
            button_size=20,
            icon_size=16,
            object_name="recordItemInfoButton",
            tooltip="Let Chronica tells you more about this record"
        )
        
        self.delete_button = icon_button(
            QIcons.get("trash.svg"),
            button_size=20,
            icon_size=16,
            object_name="recordItemDeleteButton",
            tooltip="Delete this record"
        )
        
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.info_button)
        buttons_layout.addWidget(self.delete_button)
        
        # Assemble
        self.content = QFrame(frameShape=QFrame.Shape.NoFrame)
        content_layout = QHBoxLayout(self.content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(5)
        content_layout.addWidget(self.time_labels, 0)
        content_layout.addWidget(self.icon_buttons, alignment=Qt.AlignmentFlag.AlignLeft)
        content_layout.addStretch()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 5, 12, 5)
        layout.setSpacing(5)
        layout.addWidget(self.header)
        layout.addWidget(self.content)
        
        self.info_button.clicked.connect(self._on_info_button_clicked)
        self.delete_button.clicked.connect(self._on_delete_button_clicked)
        self.setStyleSheet(Stylesheets.load("tracking_record_item_widget.qss"))
    
    @Slot()
    def _on_info_button_clicked(self) -> None:
        self.explain_record_requested.emit(self.record)

        self.chronica.say_random(
            scenario=Scenario.BRIEFLY_TALK_ABOUT_A_RECORD,
            context=self._generate_dialogue_context()
        )

    @Slot()
    def _on_delete_button_clicked(self) -> None:
        chronica_judge: str = "Chronica: Forgive my creator for how useless he is that he couldn't make me interact with this delete event."
        chronica_judge2: str = "But well, he indeed tried his best."
        
        box = QMessageBox(self)
        box.setWindowTitle("Delete tracking record")
        box.setText(f"Are you sure you want to delete this tracking record '{self.record.title}'?\n\n{chronica_judge}\n{chronica_judge2}")
        box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        box.setDefaultButton(QMessageBox.StandardButton.No)
        box.setIcon(QMessageBox.Icon.Question)
        box.finished.connect(self._on_message_box_finished)
        box.open()
    
    @Slot()
    def _on_message_box_finished(self, result: int) -> None:
        if result == QMessageBox.StandardButton.Yes:
            self.delete_record_requested.emit(self.record.title, self)

    def _generate_dialogue_context(self) -> DialogueRenderContext:
        return DialogueRenderContextBuilder() \
            .with_line_render_context(
                "explain_record",
                record_title=self.record.title,
                record_generated_at=ymd_hms(self.record.generated_at),
                record_started_at=ymd_hms(self.record.start),
                record_stopped_at=ymd_hms(self.record.end),
                record_duration=human_readable(self.record.duration)
            ) \
            .with_line_render_context(
                "explain_record_description",
                record_description=self.record.description
            ) \
            .build()