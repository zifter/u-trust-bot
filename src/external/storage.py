import logging

from google.cloud import datastore, ndb

logger = logging.getLogger('storage')


class User(ndb.Model):
    telegram_id = ndb.IntegerProperty()

    @classmethod
    def query_by_telegram_id(cls, telegram_id):
        return cls.query(cls.telegram_id == telegram_id)


class Storage:
    USER = 'User'

    def __init__(self):
        self.client = ndb.Client()

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
