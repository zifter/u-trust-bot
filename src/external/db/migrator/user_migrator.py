from typing import Dict

from external.db.migrator.base import MigratorBase
from external.db.models import Analytics, User, CommandState


class UserMigrator(MigratorBase):
    def __init__(self):
        super().__init__()
        self.migrations: Dict[int, callable] = {
            1: self.migration_0_to_1,
            2: self.migration_1_to_2,
            3: self.migration_2_to_3,
        }

    def migration_0_to_1(self, user: User):
        user.analytics = Analytics()

    def migration_1_to_2(self, user: User):
        user.command_state = CommandState(name='', state={})

    def migration_2_to_3(self, user: User):
        # reset failed messages because it's not working properly
        user.analytics.failed_messages = 0
