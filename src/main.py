import argparse
import logging
import os

from argparse import ArgumentParser

from external.gcp import GCP
from external.storage import Storage
from external.tg import Telegram
from external.facade import ExternalAPIFacade

from utrust.bot import Bot


logger = logging.getLogger('u-trust-bot')


def env_var(env, default=None, prefix='TRUST_'):
    return os.environ.get(f'{prefix}{env}', default)


def get_args():
    parser = ArgumentParser()
    parser.add_argument("--environment-name", default=env_var('ENVIRONMENT_NAME', 'staging'), type=str)
    parser.add_argument("--webhook", default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument("--telegram-token", default=env_var('TELEGRAM_TOKEN', None))
    parser.add_argument("--secret-token", default=env_var('SECRET_TOKEN', None), type=str)
    parser.add_argument("--url", default=env_var('URL', None), type=str)
    parser.add_argument("--port", default=int(env_var('PORT', 8080)), type=int)
    parser.add_argument("--language", default=env_var('LANGUAGE', "ru-RU"), type=str)

    parser.add_argument("--speech-to-text-workspace", default=env_var('SPEECH_TO_TEXT_WORKSPACE', None))

    return parser.parse_args()


def main(environment_name: str,
         webhook: bool,
         telegram_token: str,
         speech_to_text_workspace: str,
         port: int,
         secret_token: str,
         language: str,
         url: str):
    logger.info('Start bot')

    facade = ExternalAPIFacade(
        gcp=GCP(speech_to_text_workspace, language),
        tg=Telegram(telegram_token),
        db=Storage(environment_name)
    )

    bot = Bot(facade)
    if webhook:
        bot.run_webhook(port, secret_token, url)
    else:
        bot.run_polling()


if __name__ == '__main__':
    args = get_args()
    logger.info(args)
    main(**vars(args))
