from typing import Any, Literal, Optional
from pydantic import BaseModel
from .common import StateCount


class ServerLicenseCount(BaseModel):
    available_global: Optional[int] = 0
    available_local: Optional[int] = 0
    used: Optional[int] = 0
    high_use: Optional[int] = 0

    @classmethod
    def from_string(cls, data: str) -> "ServerLicenseCount":
        values = {
            p.split(":")[0]: int(p.split(":")[1]) for p in data.split(" ") if ":" in p
        }
        return ServerLicenseCount(
            available_global=values.get("Avail_Global", 0),
            available_local=values.get("Avail_Local", 0),
            used=values.get("Used", 0),
            high_use=values.get("High_Use", 0),
        )


class Server(BaseModel):
    id: str
    acl_host_enable: Optional[bool] = False
    acl_host_moms_enable: Optional[bool] = False
    acl_hosts: Optional[str] = None
    acl_resv_group_enable: Optional[bool] = False
    acl_resv_groups: Optional[str] = None
    acl_resv_host_enable: Optional[bool] = False
    acl_resv_hosts: Optional[str] = None
    acl_resv_user_enable: Optional[bool] = False
    acl_resv_users: Optional[str] = None
    acl_roots: Optional[str] = None
    acl_user_enable: Optional[bool] = False
    acl_users: Optional[str] = None
    backfill_depth: Optional[int] = 1
    comment: Optional[str] = None
    default_chunk: Optional[dict[str, Any]] = {}
    default_qdel_arguments: Optional[str] = None
    default_qsub_arguments: Optional[str] = None
    default_queue: Optional[str] = "workq"
    eligible_time_enable: Optional[bool] = False
    flatuid: Optional[bool] = False
    FLicenses: Optional[int] = None
    job_history_duration: Optional[str] = None
    job_history_enable: Optional[bool] = False
    job_requeue_timeout: Optional[str] = None
    job_sort_formula: Optional[str] = None
    jobscript_max_size: Optional[str] = "100000000"
    license_count: Optional[ServerLicenseCount] = ServerLicenseCount()
    log_events: Optional[int] = 511
    mail_from: Optional[str] = "adm"
    managers: Optional[str] = None
    max_array_size: Optional[int] = 10000
    max_concurrent_provision: Optional[int] = 5
    max_group_res: Optional[str] = None
    max_group_res_soft: Optional[str] = None
    max_group_run: Optional[int] = None
    max_group_run_soft: Optional[int] = None
    max_queued: Optional[str] = None
    max_queued_res: Optional[str] = None
    max_run: Optional[str] = None
    max_run_res: Optional[str] = None
    max_run_res_soft: Optional[str] = None
    max_run_soft: Optional[str] = None
    max_running: Optional[int] = None
    max_user_res: Optional[str] = None
    max_user_res_soft: Optional[str] = None
    max_user_run: Optional[int] = None
    max_user_run_soft: Optional[int] = None
    node_fail_requeue: Optional[int] = 310
    node_group_enable: Optional[bool] = False
    node_group_key: Optional[str] = None
    operators: Optional[str] = None
    pbs_license_info: Optional[str] = None
    pbs_license_linger_time: Optional[int] = 3600
    pbs_license_max: Optional[int] = 2147483647
    pbs_license_min: Optional[int] = 0
    pbs_version: Optional[str] = None
    power_provisioning: Optional[bool] = False
    python_restart_max_hooks: Optional[int] = 100
    python_restart_max_objects: Optional[int] = 1000
    python_restart_min_interval: Optional[int] = 30
    query_other_jobs: Optional[bool] = True
    queued_jobs_threshold: Optional[str] = None
    queued_jobs_threshold_res: Optional[str] = None
    reserve_retry_init: Optional[int] = 7200
    reserve_retry_time: Optional[int] = 600
    resources_assigned: Optional[dict[str, Any]] = {}
    resources_available: Optional[dict[str, Any]] = {}
    resources_default: Optional[dict[str, Any]] = {}
    resources_max: Optional[dict[str, Any]] = {}
    restrict_res_to_release_on_suspend: Optional[str] = None
    resv_enable: Optional[bool] = True
    resv_post_processing_time: Optional[int] = None
    rpp_highwater: Optional[int] = 1024
    rpp_max_pkt_check: Optional[int] = 1024
    rpp_retry: Optional[int] = 10
    scheduler_iteration: Optional[int] = 600
    scheduling: Optional[bool] = False
    server_host: Optional[str] = None
    server_state: Optional[
        Literal[
            "Active",
            "Hot_Start",
            "Idle",
            "Scheduling",
            "Terminating",
            "Terminating_Delayed",
        ]
    ] = None
    state_count: Optional[StateCount] = StateCount()
    total_jobs: Optional[int] = 0

    @classmethod
    def from_pbs(cls, data: dict[str, str]) -> "Server":
        for key in [
            "resources_assigned",
            "resources_available",
            "resources_default",
            "resources_max",
            "default_chunk",
        ]:
            keys = [k.split(".")[1] for k in data.keys() if k.startswith(key + ".")]
            data[key] = {}
            for k in keys:
                try:
                    data[key][k] = int(data[key + "." + k])
                except:
                    data[key][k] = data[key + "." + k]

        data["license_count"] = (
            ServerLicenseCount.from_string(data["license_count"])
            if "license_count" in data.keys()
            else ServerLicenseCount()
        )
        data["state_count"] = (
            StateCount.from_string(data["state_count"])
            if "state_count" in data.keys()
            else StateCount()
        )

        return Server(**data)
