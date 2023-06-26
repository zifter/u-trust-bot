import abc
from typing import final, Optional, List

from utrust.actions import logger


class ActionBase:
    def __init__(self):
        self.permissions = []

    @final
    async def exec(self):
        logger.info(f'Execute {self.__class__}. Start')

        actions = await self.do_exec()
        if actions:
            if isinstance(actions, ActionBase):
                await actions.exec()
            elif isinstance(actions, list):
                for cmd in actions:
                    await cmd.exec()
            else:
                raise ValueError()

        logger.info(f'Execute {self.__class__.__name__}. End')

    @abc.abstractmethod
    async def do_exec(self) -> Optional[List['ActionBase']]:
        raise NotImplemented()
