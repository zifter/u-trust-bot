import asyncio

from telegram import Message
from telethon.tl.custom import Conversation


class UTrustUser:
    YOU_ACCOUNT_IS_DELETED_TEXT = 'You account is deleted'
    AUTHORIZATION_TOKEN = 'I-trust-U'

    YOU_ARE_NOT_AUTHORIZED_TEXT = 'You are not authorized. Please, send me authorization code'
    YOU_ARE_ALREADY_AUTHORIZED_TEXT = 'You are already authorized'

    NO_ACTIVE_COMMAND = "No active command to cancel. I wasn't doing anything anyway. Zzzzz..."
    WRONG_AUTH_TOKEN_TEXT = 'Wrong auth token. Please, send me authorization code'
    AUTHORIZED_CONGRATULATIONS_TEXT = 'Thanks! You are authorized to work with me'

    def __init__(self, conv: Conversation):
        self.conv = conv

    async def authorize(self):
        _ = await self.command_cancel()
        resp = await self.command_auth()

        if resp.text == UTrustUser.YOU_ARE_NOT_AUTHORIZED_TEXT:
            await self.send_text_message_ang_get_response(UTrustUser.AUTHORIZATION_TOKEN)
        elif resp.text == UTrustUser.YOU_ARE_ALREADY_AUTHORIZED_TEXT:
            pass
        else:
            assert False, f'Unknown state: {resp.text}'

    async def delete_conversation(self):
        _ = await self.command_cancel()
        _ = await self.command_forget_me()

    async def command_start(self) -> Message:
        return await self.send_text_message_ang_get_response('/start')

    async def command_auth(self) -> Message:
        return await self.send_text_message_ang_get_response('/auth')

    async def command_forget_me(self) -> Message:
        return await self.send_text_message_ang_get_response('/forgetme')

    async def command_info(self) -> Message:
        return await self.send_text_message_ang_get_response('/info')

    async def command_cancel(self) -> Message:
        return await self.send_text_message_ang_get_response('/cancel')

    async def send_text_message_ang_get_response(self, text) -> Message:
        await asyncio.sleep(0.3)
        await self.conv.send_message(text)
        await asyncio.sleep(0.2)
        return await self.conv.get_response()

    async def send_file_message_ang_get_response(self, fl) -> Message:
        await asyncio.sleep(1)
        await self.conv.send_file(fl)
        await asyncio.sleep(0.2)
        return await self.conv.get_response()

    def is_info_text(self, text) -> bool:
        return "Joined:" in text

    def is_not_autorized_text(self, text) -> bool:
        return text == UTrustUser.YOU_ARE_NOT_AUTHORIZED_TEXT

    def is_canceled_text(self, text, command) -> bool:
        return text == f'The command {command} has been cancelled. Anything else I can do for you?\n\n' \
                       f'Send /help for a list of commands.'
