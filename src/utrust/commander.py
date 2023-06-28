from dataclasses import dataclass
from typing import List, Type

from external.tg import BotCommand


@dataclass
class Command:
    action: Type['UserActionBase']

    show_in_help: bool = True


@dataclass
class Section:
    name: str
    commands: List[Command]


class Commander:
    def __init__(self, layout, welcome_text):
        self._layout: List[Section] = layout
        self._hello_text = welcome_text

    def help_description(self):
        return f"{self._hello_text}" \
               f"\n\nYou can control me by sending these commands:" \
               f"\n{self._commands_list_descr()}"

    @property
    def commands(self) -> List[Command]:
        return [cmd for section in self._layout for cmd in section.commands]

    def get_action_class(self, command_name) -> 'UserActionBase':
        for cmd in self.commands:
            if command_name == cmd.action.COMMAND_NAME:
                return cmd.action

    def telegram_bot_commands(self) -> List[BotCommand]:
        return [BotCommand(cmd.action.COMMAND_NAME, cmd.action.COMMAND_DESCR) for cmd in self.commands]

    def _commands_list_descr(self):
        r = ''
        for s in self._layout:
            r += f'\n<b>{s.name}</b>\n'
            r += '\n'.join(f'/{cmd.action.COMMAND_NAME} {cmd.action.COMMAND_DESCR}' for cmd in s.commands if cmd.show_in_help)
            r += '\n'

        r = r[:-1]

        return r
