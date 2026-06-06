from enum import Enum, auto
import random

from src.chronica.characters.models import (
    Line,
    RenderedDialogue,
    DialogueTemplate,
    DialogueKey
)

class Scenario(Enum):
    BOOTUP = auto()
    SHUTDOWN = auto()
    SYSTEM_CRASH = auto()
    EXCEPTION = auto()
    PORTRAIT_INTERACTION = auto()
    START_TRACKING = auto()
    STOP_TRACKING = auto()
    PRAISE = auto()
    REMIND = auto()
    IDLE_IN_CHRONICA = auto()
    SMALL_TALK = auto()

type DialogueDatabase = dict[Scenario, dict[DialogueKey, DialogueTemplate]]

CHRONICA_DIALOGUE_DATABASE: DialogueDatabase = {
    Scenario.BOOTUP: {
        "bootup_1": DialogueTemplate(
            key="bootup_1",
            lines=[
                Line(key="bootup_1.line_1", text="Welcome to Chronica!"),
                Line(key="bootup_1.line_2", text="This is a test message for early development of dialogue system."),
                Line(key="bootup_1.line_3", text="No users should ever see this. :)")
            ]
        )
    }
}