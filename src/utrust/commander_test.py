from utrust.actions.app.message.user.base import UserActionBase
from utrust.commander import Commander, Section, Command


class CommandTestStart(UserActionBase):
    COMMAND_NAME = 'start'
    COMMAND_DESCR = 'my start descr'


class CommandTestAction(UserActionBase):
    COMMAND_NAME = 'action1'
    COMMAND_DESCR = 'my action1 descr'


class CommandTestAction2(UserActionBase):
    COMMAND_NAME = 'action2'
    COMMAND_DESCR = 'my action2 descr'



test_layout = [
    Section('First', [
        Command(CommandTestStart),
    ]),
    Section('Second', [
        Command(CommandTestAction),
        Command(CommandTestAction2),
    ])
]


def test_commander_get_start_description():
    cmder = Commander(test_layout, 'Hello World!')

    got = cmder.start_description()
    expected = "Hello World!" \
               "\n\nYou can control me by sending these commands:" \
               "\n\n<b>First</b>" \
               "\n/start my start descr" \
               "\n\n<b>Second</b>" \
               "\n/action1 my action1 descr" \
               "\n/action2 my action2 descr"

    assert got == expected
