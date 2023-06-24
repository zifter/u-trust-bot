import inspect
import logging
from typing import Dict

from external.db.models import Analytics, User

logger = logging.getLogger('migrator')


class Migrator:
    def __init__(self):
        self.migrations: Dict[int, callable] = {
            1: self.migration_0_to_1,
        }

    @property
    def latest_version(self):
        return max(self.migrations.keys())

    def migrate(self, user: User) -> User:
        user_version = user.version if user.version else 0
        for version in range(user_version, self.latest_version, 1):
            user = self.migrate_to(user, version + 1)

        return user

    def migrate_to(self, user, version) -> User:
        logger.info(f'Migrate {user} to {version}')
        migration = self.migrations[version]
        migration(user)
        user.version = version
        return user

    def migration_0_to_1(self, user):
        user.analytics = Analytics()
