import logging

from google.cloud import ndb

from external.db.types import User

logger = logging.getLogger('storage')


class Storage:
    USER = 'User'

    def __init__(self, namespace):
        self.client = ndb.Client(namespace=namespace)

    def get_user(self, telegram_id):
        logger.info(f'Create user {telegram_id}')

        with self.client.context():
            query = User.query_by_telegram_id(telegram_id)
            for user in query:
                return user

        return None

    def create_user(self, user: User):
        logger.info(f'Create user {user}')

        with self.client.context():
            user.put()
