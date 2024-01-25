from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel


class QueueTypeLong(Enum):
    EXECUTION = "Execution"
    ROUTING = "Routing"


class QueueTypeShort(Enum):
    EXECUTION = "E"
    ROUTING = "R"


QueueType = Union[QueueTypeLong, QueueTypeShort]


class StateCount(BaseModel):
    transit: Optional[int] = 0
    queued: Optional[int] = 0
    held: Optional[int] = 0
    waiting: Optional[int] = 0
    running: Optional[int] = 0
    exiting: Optional[int] = 0
    begun: Optional[int] = 0

    @classmethod
    def from_string(cls, data: str) -> "StateCount":
        values = {
            p.split(":")[0].lower(): int(p.split(":")[1])
            for p in data.split(" ")
            if ":" in p
        }
        return StateCount(**values)
