from external.db.migrator import Migrator
from external.db.models import User, Registration
from external.db.storage import Storage


def test_new_user_is_equal_migration():
    storage = Storage('test')
    new_user = storage.create_new_user(1234)

    user = User(
        telegram_id=1234,
        registration=Registration(
            created_at=new_user.registration.created_at
        )
    )

    migrator = Migrator()
    migrated_user = migrator.migrate(user)
    assert migrated_user == new_user

