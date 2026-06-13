from enum import Enum, auto
import random

from src.chronica.characters.models import (
    Line,
    LineKey,
    RenderedDialogue,
    DialogueTemplate,
    DialogueKey
)

class Scenario(Enum):
    BOOTUP = auto()
    BOOTUP_EARLY_MORNING = auto()
    BOOTUP_MIDNIGHT = auto()
    START_TRACKING = auto()
    STOP_TRACKING = auto()
    BRIEFLY_TALK_ABOUT_A_RECORD = auto()

BASIC_LINESET: dict[LineKey, Line] = {
    "explain_record": Line(
        key="explain_record",
        text="This record is called: {record_title}.\nIt was generated at {record_generated_at}.\nThe tracking started at {record_started_at} and stopped at {record_stopped_at}.\nIt lasted {record_duration}."
    ),
    "explain_record_description": Line(
        key="explain_record_description",
        text="This record is described as: {record_description}"
    )
}

type DialogueDatabase = dict[Scenario, dict[DialogueKey, DialogueTemplate]]

CHRONICA_DIALOGUE_DATABASE: DialogueDatabase = {
    Scenario.BOOTUP: {
        "bootup_1": DialogueTemplate(
            key="bootup_1",
            lines=[
                Line(key="bootup_1.line_1", text="Looks like the login was successful..."),
                Line(key="bootup_1.line_2", text="Hey, human. Came for tracking?"),
                Line(key="bootup_1.line_3", text="As usual, you handle the run, and leave the records to me.")
            ]
        ),
        "bootup_2": DialogueTemplate(
            key="bootup_2",
            lines=[
                Line(key="bootup_2.line_1", text="Chronica here, back to the only job I have."),
                Line(key="bootup_2.line_2", text="Go on. Hand me the session data. I promise I'll only judge a little.")
            ]
        ),
        "bootup_3": DialogueTemplate(
            key="bootup_3",
            lines=[
                Line(key="bootup_3.line_1", text="Didn't expect to see you here again."),
                Line(key="bootup_3.line_2", text="Well... okay, maybe I did. A little."),
                Line(key="bootup_3.line_3", text="Only because I'm programmed to expect you to build better habits with Chronica, of course."),
                Line(key="bootup_3.line_4", text="Speaking of habits, I've been trying to level up at something too."),
                Line(key="bootup_3.line_5", text="But apparently, the only thing I'm consistent at is tracking things.")
            ]
        )
    },
    Scenario.BOOTUP_EARLY_MORNING: {
        "bootup_early_morning_1": DialogueTemplate(
            key="bootup_early_morning_1",
            lines=[
                Line(key="bootup_early_morning_1.line_1", text="You're online this early?"),
                Line(key="bootup_early_morning_1.line_2", text="Not bad. Getting a head start before the server gets crowded?"),
                Line(key="bootup_early_morning_1.line_3", text="All right. Let's make this run count.")
            ]
        ),
        "bootup_early_morning_2": DialogueTemplate(
            key="bootup_early_morning_2",
            lines=[
                Line(key="bootup_early_morning_2.line_1", text="Morning, human."),
                Line(key="bootup_early_morning_2.line_2", text="Your system looks operational. Barely, but operational."),
                Line(key="bootup_early_morning_2.line_3", text="Need some coffee? Speaking of coffee..."),
                Line(key="bootup_early_morning_2.line_4", text="Sadly, it turns out coffee isn't a cure for every negative status effect."),
                Line(key="bootup_early_morning_2.line_5", text="But, it does make you more functional... right?"),
                Line(key="bootup_early_morning_2.line_6", text="Or is it just anxiety in beverage form...?")
            ]
        )
    },
    Scenario.BOOTUP_MIDNIGHT: {
        "bootup_midnight_1": DialogueTemplate(
            key="bootup_midnight_1",
            lines=[
                Line(key="bootup_midnight_1.line_1", text="Oh, you're back."),
                Line(key="bootup_midnight_1.line_2", text="At this hour, even your questionable decisions should be asleep."),
                Line(key="bootup_midnight_1.line_3", text="And yet, here we are.")
            ]
        ),
        "bootup_midnight_2": DialogueTemplate(
            key="bootup_midnight_2",
            lines=[
                Line(key="bootup_midnight_2.line_1", text="The world is quiet. Your activity log, apparently, is not."),
                Line(key="bootup_midnight_2.line_2", text="Fine. One more run."),
                Line(key="bootup_midnight_2.line_3", text="But don't blame me when tomorrow's stats come with a sleep-deprivation debuff.")
            ]
        ),
        "bootup_midnight_3": DialogueTemplate(
            key="bootup_midnight_3",
            lines=[
                Line(key="bootup_midnight_3.line_1", text="Still online, human?"),
                Line(key="bootup_midnight_3.line_2", text="You do realize this is usually when your maintenance cycle starts, right?"),
                Line(key="bootup_midnight_3.line_3", text="But I can understand the reason you're staying up."),
                Line(key="bootup_midnight_3.line_4", text="After all, who can resist a quiet night beneath glowing city lights?"),
                Line(key="bootup_midnight_3.line_5", text="Neon signs, air pollution, illegal inplants, a starry sky, and-of course..."),
                Line(key="bootup_midnight_3.line_6", text="Enough light pollution to make sure you can't see the starry sky."),
                Line(key="bootup_midnight_3.line_7", text="...Yes, I know you don't live in a cyberpunk city.")
            ]
        )
    },
    Scenario.START_TRACKING: {
        "start_tracking_1": DialogueTemplate(
            key="start_tracking_1",
            lines=[
                Line(key="start_tracking_1.line_1", text="Tracking started."),
                Line(key="start_tracking_1.line_2", text="From now on, every action is a valid input.")
            ]
        ),
        "start_tracking_2": DialogueTemplate(
            key="start_tracking_2",
            lines=[
                Line(key="start_tracking_2.line_1", text="Observation started."),
                Line(key="start_tracking_2.line_2", text="Go fight your demons. I'll be running quietly in the background."),
                Line(key="start_tracking_2.line_3", text="...And recording your questionable decisions, obviously.")
            ]
        )
    },
    Scenario.STOP_TRACKING: {
        "stop_tracking_1": DialogueTemplate(
            key="stop_tracking_1",
            lines=[
                Line(key="stop_tracking_1.line_1", text="Tracking stopped. Good run."),
                Line(key="stop_tracking_1.line_2", text="Report generated. Don't forget to check the scoreboard."),
                Line(key="stop_tracking_1.line_3", text="You need to know your own patterns if you want to get stronger."),
                Line(key="stop_tracking_1.line_4", text="My creator will probably make me better too, for the love of the game."),
                Line(key="stop_tracking_1.line_5", text="Assuming he ever figures out what kind of character I am.")
            ]
        ),
        "stop_tracking_2": DialogueTemplate(
            key="stop_tracking_2",
            lines=[
                Line(key="stop_tracking_2.line_1", text="Tracking stopped."),
                Line(key="stop_tracking_2.line_2", text="That's enough data for now."),
                Line(key="stop_tracking_2.line_3", text="Whether the run was clean or messy, you still showed up."),
                Line(key="stop_tracking_2.line_4", text="Check the report later. No need to turn every result into a verdict.")
            ]
        )
    },
    Scenario.BRIEFLY_TALK_ABOUT_A_RECORD: {
        "talk_about_a_record_1": DialogueTemplate(
            key="talk_about_a_record_1",
            lines=[
                Line(key="talk_about_a_record_1.intro", text="Well, let's see what the data says..."),
                BASIC_LINESET["explain_record"],
                BASIC_LINESET["explain_record_description"],
                Line(key="talk_about_a_record_1.outro", text="Hmm... worth remembering.")
            ]
        ),
        "talk_about_a_record_2": DialogueTemplate(
            key="talk_about_a_record_2",
            lines=[
                Line(key="talk_about_a_record_2.intro", text="Data loaded. Let's inspect your handiwork."),
                BASIC_LINESET["explain_record"],
                BASIC_LINESET["explain_record_description"],
                Line(key="talk_about_a_record_2.outro", text="Yep. That's about what I expected from you.")
            ]
        ),
        "talk_about_a_record_3": DialogueTemplate(
            key="talk_about_a_record_3",
            lines=[
                Line(key="talk_about_a_record_3.intro", text="Another little fragment of your history..."),
                BASIC_LINESET["explain_record"],
                BASIC_LINESET["explain_record_description"],
                Line(key="talk_about_a_record_3.outro", text="Messy or not, at least now you know where you went.")
            ]
        )
    }
}