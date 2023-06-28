from telegram import BotCommand

from utrust.actions.app.message.user.base import UserActionBase
from utrust.commander import Commander, Section, Command


class CommandTestStart(UserActionBase):
    COMMAND_NAME = 'start'
    COMMAND_DESCR = 'my start descr'


class CommandTestAction1(UserActionBase):
    COMMAND_NAME = 'action1'
    COMMAND_DESCR = 'my action1 descr'


class CommandTestAction2(UserActionBase):
    COMMAND_NAME = 'action2'
    COMMAND_DESCR = 'my action2 descr'


class CommandTestAction3(UserActionBase):
    COMMAND_NAME = 'action3'
    COMMAND_DESCR = 'my action3 descr'


test_layout = [
    Section('First', [
        Command(CommandTestStart),
    ]),
    Section('Second', [
        Command(CommandTestAction1),
        Command(CommandTestAction2),
        Command(CommandTestAction3, show_in_help=False),
    ])
]

welcome_text = "Welcome to the bot!"


def test_start_description():
    cmder = Commander(test_layout, welcome_text)

    got = cmder.help_description()
    expected = "Welcome to the bot!" \
               "\n\nYou can control me by sending these commands:" \
               "\n\n<b>First</b>" \
               "\n/start my start descr" \
               "\n\n<b>Second</b>" \
               "\n/action1 my action1 descr" \
               "\n/action2 my action2 descr"

    assert got == expected


def test_commands():

    commander = Commander(test_layout, welcome_text)

    expected_commands = [
        Command(CommandTestStart),
        Command(CommandTestAction1),
        Command(CommandTestAction2),
        Command(CommandTestAction3, show_in_help=False),
    ]
    assert commander.commands == expected_commands


def test_get_action_class():
    commander = Commander(test_layout, welcome_text)

    assert commander.get_action_class('action1') == CommandTestAction1


def test_get_action_class_none():
    commander = Commander(test_layout, welcome_text)

    assert commander.get_action_class('fake_command') == None


def test_telegram_bot_commands():
    commander = Commander(test_layout, welcome_text)

    expected_bot_commands = [
        BotCommand('start', 'my start descr'),
        BotCommand('action1', 'my action1 descr'),
        BotCommand('action2', 'my action2 descr'),
        BotCommand('action3', 'my action3 descr')
    ]
    assert commander.telegram_bot_commands() == expected_bot_commands
