from typing import Dict

from external.db.migrator.base import MigratorBase
from utrust.context import AppContext


class AppMigrator(MigratorBase):
    def __init__(self):
        super().__init__()
        self.migrations: Dict[int, callable] = {
            1: self.migration_0_to_1,
        }

    def migration_0_to_1(self, app, app_context: AppContext):
        pass

