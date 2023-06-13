from external.gcp import GCP
from external.db.storage import Storage
from external.tg import Telegram


class ExternalAPIFacade:
    def __init__(self, gcp: GCP, tg: Telegram, db: Storage):
        self.gcp = gcp
        self.tg = tg
        self.db = db
