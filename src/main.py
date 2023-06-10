import os

from argparse import ArgumentParser

from external.gcp import GCPFacade
from external.tg import TelegramFacade
from utrust.bot import UTrustBot


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--webhook", default=True, type=bool)
    parser.add_argument("--telegram-token", default=os.environ.get('UTRUST_TELEGRAM_TOKEN', None))
    parser.add_argument("--secret-token", default=os.environ.get('UTRUST_SECRET_TOKEN', None), type=str)
    parser.add_argument("--url", default=os.environ.get('UTRUST_URL', None), type=str)
    parser.add_argument("--port", default=int(os.environ.get("PORT", 8080)), type=int)

    parser.add_argument("--speech-to-text-workspace", default=os.environ.get('UTRUST_SPEECH_TO_TEXT_WORKSPACE', None))
    return parser.parse_args()


def main(webhook: bool, telegram_token: str, speech_to_text_workspace: str, port: int, secret_token: str, url: str):
    gcp = GCPFacade(speech_to_text_workspace)
    tg = TelegramFacade(telegram_token)

    bot = UTrustBot(gcp, tg)
    if webhook:
        bot.run_webhook(port, secret_token, url)
    else:
        bot.run_polling()


if __name__ == '__main__':
    args = get_args()
    main(**vars(args))
