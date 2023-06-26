from external.gcp.facade import GCPFacade
from external.db.facade import StorageFacade
from external.tg.facade import TelegramFacade


class ExternalAPI:
    def __init__(self, gcp: GCPFacade, tg: TelegramFacade, db: StorageFacade):
        self.gcp = gcp
        self.tg = tg
        self.db = db
