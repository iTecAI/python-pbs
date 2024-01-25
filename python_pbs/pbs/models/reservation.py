from enum import Enum
from typing import Optional
from pydantic import BaseModel


class ReservationState(Enum):
    NONE = "NO"
    UNCONFIRMED = "UN"
    CONFIRMED = "CO"
    WAIT = "WT"
    TIME_TO_RUN = "TR"
    RUNNING = "RN"
    FINISHED = "FN"
    BEING_DELETED = "BD"
    DELETED = "DE"
    DELETING_JOBS = "DJ"


class Reservation(BaseModel):
    id: Optional[str] = None
    authorized_groups: Optional[str] = None
    authorized_hosts: Optional[str] = None
    authorized_users: Optional[str] = None
    ctime: Optional[int] = None
    interactive: Optional[int] = 0
    mail_points: Optional[str] = "n"
    mail_users: Optional[str] = None
    mtime: Optional[int] = None
    queue: Optional[str] = None
    reserve_count: Optional[int] = None
    reserve_duration: Optional[int] = None
    reserve_end: Optional[int] = None
    reserve_id: Optional[str] = None
    reserve_index: Optional[int] = None
    reserve_job: Optional[str] = None
    reserve_name: Optional[str] = None
    reserve_owner: Optional[str] = None
    reserve_retry: Optional[int] = None
    reserve_rrule: Optional[str] = None
    reserve_start: Optional[int] = None
    reserve_state: Optional[ReservationState] = None
    reserve_substate: Optional[int] = None
    resource_list: Optional[dict] = {}
    resv_nodes: Optional[str] = None
    server: Optional[str] = None

    @classmethod
    def from_pbs(cls, data: dict[str, str]) -> "Reservation":
        for key in [
            "resource_list",
        ]:
            keys = [k.split(".")[1] for k in data.keys() if k.startswith(key + ".")]
            data[key] = {}
            for k in keys:
                data[key][k] = int(data[key + "." + k])

        return Reservation(**{k.lower(): v for k, v in data.items()})
