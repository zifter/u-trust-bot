import abc
from typing import final, Optional, List

from utrust.actions import logger


class ActionBase:
    def __init__(self):
        self.permissions = []

    @final
    async def exec(self):
        logger.info(f'Execute {self.__class__}. Start')

        await self.pre_exec()

        failed_to_exec = False
        try:
            actions = await self.do_exec()
            if actions:
                if isinstance(actions, ActionBase):
                    await actions.exec()
                elif isinstance(actions, list):
                    for cmd in actions:
                        await cmd.exec()
                else:
                    raise ValueError()
        except Exception as e:
            logger.exception('Failed to execute')
            raise
        finally:
            await self.post_exec(failed_to_exec)

        logger.info(f'Execute {self.__class__.__name__}. End')

    async def pre_exec(self):
        pass

    @abc.abstractmethod
    async def do_exec(self) -> Optional[List['ActionBase']]:
        raise NotImplemented()

    async def post_exec(self, failed_to_exec):
        pass
