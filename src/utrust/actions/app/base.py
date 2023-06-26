from pathlib import Path

from external import ExternalAPI
from utrust.actions.base import ActionBase
from utrust.context import AppContext


class AppActionBase(ActionBase):
    def __init__(self, app_context: AppContext):
        super().__init__()

        self.app_context = app_context

    @property
    def external(self) -> ExternalAPI:
        return self.app_context.external

    @property
    def tmp_dir(self) -> Path:
        return self.app_context.tmp_dir

