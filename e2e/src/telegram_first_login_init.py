from telethon import TelegramClient
from telethon.sessions import StringSession

from settings import TELEGRAM_APP_ID, TELEGRAM_APP_HASH


def main():
    with TelegramClient(StringSession(), TELEGRAM_APP_ID, TELEGRAM_APP_HASH) as client:
        print("Session string:", client.session.save())


if __name__ == '__main__':
    main()
