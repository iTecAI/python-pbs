from enum import Enum
from typing import Any, Literal, Optional
from pydantic import BaseModel


class NodeSharing(Enum):
    SHARED = "default_shared"
    EXCLUSIVE = "default_excl"
    EXCLUSIVE_HOST = "default_exclhost"
    IGNORE_EXCLUSIVE = "ignore_excl"
    FORCE_EXCLUSIVE = "force_excl"
    FORCE_EXCLUSIVE_HOST = "force_exclhost"


class NodeState(Enum):
    BUSY = "busy"
    DOWN = "down"
    FREE = "free"
    JOB_BUSY = "job-busy"
    JOB_EXCLUSIVE = "job-exclusive"
    OFFLINE = "offline"
    PROVISIONING = "provisioning"
    RESERVE_EXCLUSIVE = "resv-exclusive"
    STALE = "stale"
    STATE_UNKNOWN = "state-unknown"
    UNRESOLVABLE = "unresolvable"
    WAIT_PROVISIONING = "wait-provisioning"


class Node(BaseModel):
    id: Optional[str] = None
    comment: Optional[str] = None
    current_aoe: Optional[str] = None
    current_eoe: Optional[str] = None
    in_multivnode_host: Optional[int] = None
    jobs: Optional[Any] = None
    last_state_change_time: Optional[int] = None
    last_used_time: Optional[int] = None
    license: Optional[Literal["l"]] = None
    license_info: Optional[int] = None
    maintenance_jobs: Optional[str] = None
    mom: Optional[str] = None
    name: Optional[str] = None
    no_multinode_jobs: Optional[bool] = False
    ntype: Optional[Literal["PBS"]] = "PBS"
    partition: Optional[str] = None
    pbs_version: Optional[str] = None
    pcpus: Optional[int] = None
    pnames: Optional[str] = None
    port: Optional[int] = 15002
    poweroff_eligible: Optional[bool] = False
    power_provisioning: Optional[bool] = False
    priority: Optional[int] = None
    provision_enable: Optional[bool] = False
    resources_assigned: Optional[dict[str, Any]] = {}
    resources_available: Optional[dict[str, Any]] = {}
    resv: Optional[str] = None
    resv_enable: Optional[bool] = True
    sharing: Optional[NodeSharing] = NodeSharing.SHARED
    state: Optional[NodeState] = None
    topology_info: Optional[str] = None
    vnode_pool: Optional[int] = 0

    @classmethod
    def from_pbs(cls, data: dict[str, str]) -> "Node":
        for key in [
            "resources_assigned",
            "resources_available",
        ]:
            keys = [k.split(".")[1] for k in data.keys() if k.startswith(key + ".")]
            data[key] = {}
            for k in keys:
                data[key][k] = int(data[key + "." + k])

        return Node(**{k.lower(): v for k, v in data.items()})
