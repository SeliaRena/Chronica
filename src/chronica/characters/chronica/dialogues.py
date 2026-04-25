from enum import Enum, auto
import random

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
    
type DialogueName = str
DIALOGUES: dict[Scenario, dict[DialogueName, str]] = {
    Scenario.BOOTUP: {
        "bootup1": "Welcome to Chronica! I'm... uhh... Chronica, yeah. Anyway, I'm your time tracking assistance.",
        "bootup2": "Welcome back to Chronica. Here's your time tracking assistance... as always.",
        "bootup3": "How's it going? I hope this won't be a bit too un-professional. Anyway Chronica here."
    },
    Scenario.START_TRACKING: {
        "start1": "Chronica is now on the mission to track your time. It's bout time to lock in.",
        "start2": "Chronica -that would be me- is starting to track your app usage.",
        "start3": "I guess it's time to start another session right? Let's do this."
    },
    Scenario.STOP_TRACKING: {
        "stop1": "Keep tracking your time is not an easy task for sure, I think I need some time to... breathe.",
        "stop2": "It's been a journey, Your report is about to be generated.",
        "stop3": "Another milestone has been reached. I'm going offline to eat some ice cream. ;)"
    }
}

def random_pick_dialogue(scenario: Scenario) -> str:
    return random.choice(list(DIALOGUES[scenario].values()))

def get_dialogue(scenario: Scenario, dialogue_name: DialogueName) -> str:
    return DIALOGUES[scenario][dialogue_name]