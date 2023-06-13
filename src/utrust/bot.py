from logging import getLogger

from external.tg import Message
from utrust.context import MessageContext
from utrust.commands.flow import ProcessMessageCommand
from utrust.context import AppContext
from external.facade import ExternalAPIFacade


logger = getLogger('bot')


class Bot:
    def __init__(self, facade: ExternalAPIFacade):
        self.facade = facade
        self.app_context = AppContext(self.facade)

        self._init()

    def _init(self):
        self.facade.tg.add_message_processor(self.process_message)

    def run_polling(self):
        self.facade.tg.run_polling()

    def run_webhook(self, *args):
        self.facade.tg.run_webhook(*args)

    async def process_message(self, msg: Message):
        message_context = MessageContext(msg, self.app_context)

        cmd = ProcessMessageCommand(message_context)

        try:
            await cmd.exec()
        except Exception as e:
            logger.exception(e)
