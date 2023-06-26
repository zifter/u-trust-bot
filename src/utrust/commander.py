from dataclasses import dataclass
from typing import List, Type

from external.tg import BotCommand


@dataclass
class Command:
    name: str
    descr: str
    action: Type['UserActionBase']


@dataclass
class Section:
    name: str
    commands: List[Command]


class Commander:
    def __init__(self, layout, hello_text):
        self._layout: List[Section] = layout
        self._hello_text = hello_text

    def start_description(self):
        return f"{self._hello_text}\n\nYou can control me by sending these commands:\n{self._commands_list_descr()}"

    @property
    def commands(self) -> List[Command]:
        l = []
        for s in self._layout:
            l.extend(s.commands)

        return l

    def get_action_class(self, command_name):
        for cmd in self.commands:
            if command_name == cmd.name:
                return cmd.action

    def telegram_bot_commands(self):
        return [BotCommand(cmd.name, cmd.descr) for cmd in self.commands]

    def _commands_list_descr(self):
        r = ''
        for s in self._layout:
            r += f'\n<b>{s.name}</b>\n'
            r += '\n'.join(f'/{cmd.name} {cmd.descr}' for cmd in s.commands)
            r += '\n'

        r = r[:-1]

        return r
