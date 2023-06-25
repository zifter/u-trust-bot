from google.cloud import ndb


class Application(ndb.Model):
    version = ndb.IntegerProperty(default=0)


class Registration(ndb.Model):
    created_at = ndb.DateTimeProperty()
    confirmed = ndb.BooleanProperty(default=False)


class Analytics(ndb.Model):
    vo_total_seconds = ndb.IntegerProperty(default=0)
    processed_messages = ndb.IntegerProperty(default=0)
    failed_messages = ndb.IntegerProperty(default=0)


class User(ndb.Model):
    telegram_id = ndb.IntegerProperty()
    version = ndb.IntegerProperty()
    registration: Registration = ndb.StructuredProperty(Registration)
    analytics: Analytics = ndb.StructuredProperty(Analytics)

    @classmethod
    def query_by_telegram_id(cls, telegram_id):
        return cls.query(cls.telegram_id == telegram_id)

    def __str__(self):
        return f'User{self.telegram_id}'
