import dataclasses
import json
from dataclasses import dataclass


@dataclass
class CallbackData:
    name: str
    data: dict

    def serialize(self) -> str:
        return json.dumps(dataclasses.asdict(self))

    @staticmethod
    def deserialize(data) -> 'CallbackData':
        return CallbackData(**json.loads(data))
