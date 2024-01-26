from typing import Any, Literal, Optional
from pydantic import BaseModel
from .common import QueueType, StateCount


class Queue(BaseModel):
    id: Optional[str] = None
    acl_group_enable: Optional[bool] = False
    acl_groups: Optional[str] = None
    acl_host_enable: Optional[bool] = False
    acl_hosts: Optional[str] = None
    acl_user_enable: Optional[bool] = False
    acl_users: Optional[str] = None
    backfill_depth: Optional[int] = 1
    checkpoint_min: Optional[int] = None
    default_chunk: Optional[dict] = {}
    enabled: Optional[bool] = False
    from_route_only: Optional[bool] = False
    hasnodes: Optional[bool] = False
    kill_delay: Optional[int] = 10
    max_array_size: Optional[int] = None
    max_group_res: Optional[str] = None
    max_group_res_soft: Optional[str] = None
    max_group_run: Optional[int] = None
    max_group_run_soft: Optional[int] = None
    max_queueable: Optional[int] = None
    max_queued: Optional[str] = None
    max_queued_res: Optional[str] = None
    max_run: Optional[str] = None
    max_run_res: Optional[str] = None
    max_run_res_soft: Optional[str] = None
    max_run_soft: Optional[str] = None
    max_running: Optional[int] = None
    max_user_res: Optional[dict] = {}
    max_user_res_soft: Optional[dict] = {}
    max_user_run: Optional[int] = None
    max_user_run_soft: Optional[int] = None
    node_group_key: Optional[str] = None
    priority: Optional[int] = None
    queued_jobs_threshold: Optional[str] = None
    queue_type: Optional[QueueType] = None
    require_cred: Optional[Literal["krb5", "dce"]] = None
    require_cred_enable: Optional[bool] = False
    resources_assigned: Optional[dict[str, Any]] = {}
    resources_available: Optional[dict[str, Any]] = {}
    resources_default: Optional[dict[str, Any]] = {}
    resources_max: Optional[dict[str, Any]] = {}
    resources_min: Optional[dict[str, Any]] = {}
    route_destinations: Optional[str] = None
    route_held_jobs: Optional[bool] = False
    route_lifetime: Optional[int] = 0
    route_retry_time: Optional[int] = 30
    route_waiting_jobs: Optional[bool] = False
    started: Optional[bool] = False
    state_count: Optional[StateCount] = None
    total_jobs: Optional[int] = None

    @classmethod
    def from_pbs(cls, data: dict[str, str]) -> "Queue":
        for key in [
            "resources_assigned",
            "resources_available",
            "resources_default",
            "resources_max",
            "default_chunk",
            "resources_min",
            "max_user_res",
            "max_user_res_soft"
        ]:
            keys = [k.split(".")[1] for k in data.keys() if k.startswith(key + ".")]
            data[key] = {}
            for k in keys:
                try:
                    data[key][k] = int(data[key + "." + k])
                except:
                    data[key][k] = data[key + "." + k]

        data["state_count"] = (
            StateCount.from_string(data["state_count"])
            if "state_count" in data.keys()
            else StateCount()
        )

        return Queue(**data)
