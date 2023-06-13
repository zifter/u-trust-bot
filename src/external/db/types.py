from google.cloud import ndb


class Registration(ndb.Model):
    created_at = ndb.DateTimeProperty()
    confirmed = ndb.BooleanProperty(default=False)


class User(ndb.Model):
    telegram_id = ndb.IntegerProperty()
    registration: Registration = ndb.StructuredProperty(Registration)

    @classmethod
    def query_by_telegram_id(cls, telegram_id):
        return cls.query(cls.telegram_id == telegram_id)
