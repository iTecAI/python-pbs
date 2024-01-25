from typing import Literal, Optional
from pydantic import BaseModel


class Hook(BaseModel):
    id: Optional[str] = None
    alarm: Optional[int] = 30
    debug: Optional[bool] = False
    enabled: Optional[bool] = True
    event: Optional[str] = None
    fail_action: Optional[str] = "none"
    freq: Optional[int] = 120
    order: Optional[int] = 1
    type: Optional[Literal["pbs", "site"]] = "site"
    user: Optional[Literal["pbsadmin", "pbsuser"]] = "pbsadmin"

    @classmethod
    def from_pbs(cls, data: dict) -> "Hook":
        return Hook(**{k.lower(): v for k, v in data.items()})
