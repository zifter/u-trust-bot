from logging import getLogger
from typing import Dict


logger = getLogger('migrator')


class MigratorBase:
    def __init__(self):
        self.migrations: Dict[int, callable] = {}

    @property
    def latest_version(self):
        return max(self.migrations.keys())

    def post_migrate(self, obj, *args):
        return obj

    def migrate(self, obj, *args):
        user_version = obj.version if obj.version else 0
        for version in range(user_version, self.latest_version, 1):
            obj = self.migrate_to(obj, version + 1, *args)

        obj = self.post_migrate(obj, *args)
        return obj

    def migrate_to(self, obj, version, *args):
        logger.info(f'Migrate {obj.__class__.__name__} to {version}')
        migration = self.migrations[version]
        migration(obj, *args)
        obj.version = version
        return obj
