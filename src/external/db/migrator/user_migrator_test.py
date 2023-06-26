from unittest.mock import MagicMock

from external.db.migrator.user_migrator import UserMigrator
from external.db.models import User, Registration
from external.db.facade import StorageFacade


def test_new_user_is_equal_migration():
    storage = StorageFacade(MagicMock())
    new_user = storage.create_new_user(1234)

    user = User(
        telegram_id=1234,
        registration=Registration(
            created_at=new_user.registration.created_at
        )
    )

    migrator = UserMigrator()
    migrated_user = migrator.migrate(user)
    assert migrated_user == new_user

