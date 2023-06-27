import asyncio
from logging import getLogger

from external.tg.message import Message
from utrust.actions.app.message.user.commands.command_authorize_user import CommandAuthorizeUser
from utrust.actions.app.message.user.commands.command_forget_user import CommandForgetUser
from utrust.actions.app.message.handle_message import HandleMessageAction
from utrust.actions.app.message.user.commands.command_start import CommandStart
from utrust.actions.app.message.user.commands.command_user_info import CommandUserInfo
from utrust.app_migrator import AppMigrator
from utrust.commander import Section, Command, Commander
from utrust.context import MessageContext
from utrust.context import AppContext
from external import ExternalAPI


logger = getLogger('bot')


class BotApplication:
    def __init__(self, external: ExternalAPI):
        layout = [
            Section('Welcome', [
                Command(CommandStart),
            ]),
            Section('Account', [
                Command(CommandAuthorizeUser),
                Command(CommandUserInfo),
                Command(CommandForgetUser),
            ]),
        ]

        commander = Commander(layout, "I can help you convert you voice message to text.")

        self.app_context = AppContext(external, commander)

        self.app_context.external.tg.add_message_processor(self.process_message)

    def app_migrate(self):
        migrator = AppMigrator()
        migrator.migrate(self.app_context.external.db.get_app_state(), self.app_context)

        cmds = self.app_context.commander.telegram_bot_commands()
        asyncio.run(self.app_context.external.tg.set_my_commands(cmds))

    def run_polling(self):
        self.app_context.external.tg.run_polling()

    def run_webhook(self, *args):
        self.app_context.external.tg.run_webhook(*args)

    async def process_message(self, msg: Message):
        message_context = MessageContext(msg, self.app_context)

        cmd = HandleMessageAction(message_context)

        try:
            await cmd.exec()
        except Exception as e:
            logger.exception(e)
