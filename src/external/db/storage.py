import logging
from datetime import datetime

from external.db.migrator.user_migrator import UserMigrator
from external.db.models import User, Registration, Analytics, Application

logger = logging.getLogger('storage')


class Storage:
    USER = 'User'
    APP = 'App'

    def __init__(self, client):
        self.client = client
        self.user_migrator = UserMigrator()

    def create_new_user(self, telegram_id) -> User:
        user = User(
            telegram_id=telegram_id,
            version=self.user_migrator.latest_version,
            registration=Registration(
                created_at=datetime.now()
            ),
            analytics=Analytics(),
        )
        return user

    def get_user(self, telegram_id):
        logger.info(f'Get user {telegram_id}')

        with self.client.context():
            query = User.query_by_telegram_id(telegram_id)
            for user in query:
                return self.user_migrator.migrate(user)

        return None

    def get_app_state(self):
        with self.client.context():
            query = Application.query()
            for app in query:
                return app

            app = Application()
            app.put()
            return app

    def save_user(self, user: User):
        logger.info(f'Create user {user}')

        with self.client.context():
            user.put()
