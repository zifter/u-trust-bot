import logging
from datetime import datetime

from google.cloud import ndb

from external.db.migrator import Migrator
from external.db.models import User, Registration, Analytics

logger = logging.getLogger('storage')


class Storage:
    USER = 'User'

    def __init__(self, namespace):
        self.client = ndb.Client(namespace=namespace)
        self.migrator = Migrator()

    def create_new_user(self, telegram_id) -> User:
        user = User(
            telegram_id=telegram_id,
            version=self.migrator.latest_version,
            registration=Registration(
                created_at=datetime.now()
            ),
            analytics=Analytics(),
        )
        return user

    def get_user(self, telegram_id):
        logger.info(f'Create user {telegram_id}')

        with self.client.context():
            query = User.query_by_telegram_id(telegram_id)
            for user in query:
                return self.migrator.migrate(user)

        return None

    def save_user(self, user: User):
        logger.info(f'Create user {user}')

        with self.client.context():
            user.put()
