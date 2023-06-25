import asyncio
from logging import getLogger

from telegram import BotCommand

from external.tg import Message
from utrust.actions.command_authorize_user import CommandAuthorizeUser
from utrust.actions.command_forget_user import CommandForgetUser
from utrust.actions.command_start import CommandStart
from utrust.actions.handle_message import HandleMessageAction
from utrust.app_migrator import AppMigrator
from utrust.context import MessageContext
from utrust.context import AppContext
from external.facade import ExternalAPIFacade


logger = getLogger('bot')


class BotApplication:
    def __init__(self, facade: ExternalAPIFacade):
        self.app_context = AppContext(facade)

        self.app_context.external.tg.add_message_processor(self.process_message)
        self.commands = [
            ('start', 'Print full description for bot', CommandStart),
            ('auth', 'Authorize user to use bot', CommandAuthorizeUser),
            ('forgetme', 'Delete full data that bot aware about you', CommandForgetUser),
        ]

    def app_migrate(self):
        migrator = AppMigrator()
        migrator.migrate(self.app_context.external.db.get_app_state(), self.app_context)

        cmds = [BotCommand(name, descr) for name, descr, clazz in self.commands]
        asyncio.run(self.app_context.external.tg.set_my_commands(cmds))

    def run_polling(self):
        self.app_context.external.tg.run_polling()

    def run_webhook(self, *args):
        self.app_context.external.tg.run_webhook(*args)

    async def process_message(self, msg: Message):
        message_context = MessageContext(msg, self.app_context)

        cmd = HandleMessageAction(self.commands, message_context)

        try:
            await cmd.exec()
        except Exception as e:
            logger.exception(e)
