from typing import Literal, Optional
from pydantic import BaseModel


class Scheduler(BaseModel):
    id: Optional[str] = None
    comment: Optional[str] = None
    do_not_span_psets: Optional[bool] = False
    job_sort_formula_threshold: Optional[float] = None
    log_events: Optional[int] = 767
    only_explicit_psets: Optional[bool] = False
    opt_backfill_fuzzy: Optional[Literal["off", "low", "medium", "high"]] = "low"
    partition: Optional[str] = None
    pbs_version: Optional[str] = None
    preempt_order: Optional[str] = "SCR"
    preempt_prio: Optional[str] = "express_queue, normal_jobs"
    preempt_queue_prio: Optional[int] = 150
    preempt_sort: Optional[Literal["min_time_since_start"]] = "min_time_since_start"
    scheduler_iteration: Optional[int] = 600
    scheduling: Optional[bool] = False
    sched_cycle_length: Optional[str] = "20:00:00"
    sched_host: Optional[str] = None
    sched_log: Optional[str] = None
    sched_preempt_enforce_resumption: Optional[bool] = False
    sched_priv: Optional[str] = None
    state: Optional[Literal["down", "idle", "scheduling"]] = "down"
    throughput_mode: Optional[bool] = True

    @classmethod
    def from_pbs(cls, data: dict) -> "Scheduler":
        return Scheduler(**{k.lower(): v for k, v in data.items()})
