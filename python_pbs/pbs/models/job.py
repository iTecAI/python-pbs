from typing import Literal, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel
from enum import Enum
from .common import QueueType


class JobAccrueType(Enum):
    INITIAL_TIME = 0
    INELIGIBLE_TIME = 1
    ELIGIBLE_TIME = 2
    RUN_TIME = 3


class JobState(Enum):
    BEGUN = "B"
    EXITING = "E"
    FINISHED = "F"
    HELD = "H"
    MOVED = "M"
    QUEUED = "Q"
    RUNNING = "R"
    SUSPENDED = "S"
    TRANSITING = "T"
    USER_SUSPENDED = "U"
    WAITING = "W"
    EXPIRED = "X"


class JobJoinPath(Enum):
    MERGE_STDERR = "eo"
    MERGE_STDOUT = "oe"
    NOT_MERGED = "n"


class JobKeepFiles(Enum):
    OUTPUT = "o"
    ERROR = "e"
    RETAIN_OE = "oe"
    RETAIN_EO = "eo"
    DIRECT = "d"
    NEITHER = "n"


class JobSandbox(Enum):
    PRIVATE = "PRIVATE"
    HOME = "HOME"


class JobEstimatedValues(BaseModel):
    exec_vnode: Optional[str] = None
    soft_walltime: Optional[int] = None
    start_time: Optional[int] = None

    @classmethod
    def from_string(cls, data: str) -> "JobEstimatedValues":
        return JobEstimatedValues(**{})


class Job(BaseModel):
    id: Optional[str] = None
    account_name: Optional[str] = None
    accounting_id: Optional[str] = None
    accrue_type: Optional[JobAccrueType] = JobAccrueType.ELIGIBLE_TIME
    alt_id: Optional[str] = None
    argument_list: Optional[str] = None
    array: Optional[bool] = False
    array_id: Optional[str] = None
    array_index: Optional[int] = None
    array_indices_remaining: Optional[str] = None
    array_indices_submitted: Optional[str] = None
    array_state_count: Optional[str] = None
    block: Optional[bool] = False
    checkpoint: Optional[str] = "u"
    comment: Optional[str] = None
    create_resv_from_job: Optional[bool] = False
    ctime: Optional[int] = 0
    depend: Optional[str] = None
    egroup: Optional[str] = None
    eligible_time: Optional[int] = 0
    error_path: Optional[str] = None
    estimated: Optional[str] = None
    etime: Optional[int] = None
    euser: Optional[str] = None
    executable: Optional[str] = None
    execution_time: Optional[int] = None
    exec_host: Optional[str] = None
    exec_vnode: Optional[str] = None
    exit_status: Optional[int] = None
    forward_x11_cookie: Optional[int] = None
    forward_x11_port: Optional[bool] = False
    group_list: Optional[str] = None
    hold_types: Optional[str] = "n"
    interactive: Optional[bool] = False
    jobdir: Optional[str] = None
    job_name: Optional[str] = "STDIN"
    job_owner: Optional[str] = None
    job_state: Optional[JobState] = None
    join_path: Optional[JobJoinPath] = JobJoinPath.NOT_MERGED
    keep_files: Optional[JobKeepFiles] = JobKeepFiles.NEITHER
    mail_points: Optional[str] = "a"
    mail_users: Optional[str] = None
    max_run_subjobs: Optional[int] = None
    mtime: Optional[int] = None
    output_path: Optional[str] = None
    pcap_accelerator: Optional[int] = None
    pcap_node: Optional[int] = None
    pgov: Optional[str] = None
    priority: Optional[int] = None
    project: Optional[str] = "_pbs_project_default"
    pstate: Optional[str] = None
    qtime: Optional[int] = None
    queue: Optional[str] = None
    queue_rank: Optional[int] = None
    queue_type: Optional[QueueType] = None
    release_nodes_on_stageout: Optional[bool] = False
    remove_files: Optional[Literal["e", "o", "eo", "oe"]] = None
    rerunable: Optional[bool] = True
    resource_list: Optional[dict] = {}
    resources_released: Optional[dict] = {}
    resource_release_list: Optional[dict] = {}
    resources_used: Optional[dict] = {}
    run_count: Optional[int] = 0
    run_version: Optional[int] = None
    sandbox: Optional[JobSandbox] = JobSandbox.HOME
    schedselect: Optional[str] = None
    security_context: Optional[str] = None
    server: Optional[str] = None
    session_id: Optional[int] = None
    shell_path_list: Optional[str] = None
    stagein: Optional[str] = None
    stageout: Optional[str] = None
    stageout_status: Optional[int] = None
    stime: Optional[int] = None
    submit_arguments: Optional[str] = None
    substate: Optional[int] = None
    topjob_ineligible: Optional[bool] = False
    umask: Optional[int] = 77
    user_list: Optional[str] = None
    variable_list: Optional[str] = None

    @classmethod
    def from_pbs(cls, data: dict) -> "Job":
        for key in [
            "resource_list",
            "resources_released",
            "resource_release_list",
            "resources_used",
        ]:
            keys = [k.split(".")[1] for k in data.keys() if k.startswith(key + ".")]
            data[key] = {}
            for k in keys:
                try:
                    data[key][k] = int(data[key + "." + k])
                except:
                    data[key][k] = data[key + "." + k]
        return Job(**{k.lower(): v for k, v in data.items()})


class JobSubmission(TypedDict):
    account_name: Optional[str]
    accounting_id: Optional[str]
    accrue_type: Optional[JobAccrueType]
    alt_id: Optional[str]
    argument_list: Optional[str]
    array: Optional[bool]
    array_id: Optional[str]
    array_index: Optional[int]
    array_indices_remaining: Optional[str]
    array_indices_submitted: Optional[str]
    array_state_count: Optional[str]
    block: Optional[bool]
    checkpoint: Optional[str]
    comment: Optional[str]
    create_resv_from_job: Optional[bool]
    ctime: Optional[int]
    depend: Optional[str]
    egroup: Optional[str]
    eligible_time: Optional[int]
    error_path: Optional[str]
    estimated: Optional[str]
    etime: Optional[int]
    euser: Optional[str]
    executable: Optional[str]
    execution_time: Optional[int]
    exec_host: Optional[str]
    exec_vnode: Optional[str]
    exit_status: Optional[int]
    forward_x11_cookie: Optional[int]
    forward_x11_port: Optional[int]
    group_list: Optional[str]
    hold_types: Optional[str]
    interactive: Optional[bool]
    jobdir: Optional[str]
    job_name: Optional[str]
    job_owner: Optional[str]
    job_state: Optional[JobState]
    join_path: Optional[JobJoinPath]
    keep_files: Optional[JobKeepFiles]
    mail_points: Optional[str]
    mail_users: Optional[str]
    max_run_subjobs: Optional[int]
    mtime: Optional[int]
    output_path: Optional[str]
    pcap_accelerator: Optional[int]
    pcap_node: Optional[int]
    pgov: Optional[str]
    priority: Optional[int]
    project: Optional[str]
    pstate: Optional[str]
    qtime: Optional[int]
    queue: Optional[str]
    queue_rank: Optional[int]
    queue_type: Optional[QueueType]
    release_nodes_on_stageout: Optional[bool]
    remove_files: Optional[Literal["e", "o", "eo", "oe"]]
    rerunable: Optional[bool]
    resource_list: Optional[str]
    resources_released: Optional[str]
    resource_release_list: Optional[str]
    resources_used: Optional[str]
    run_count: Optional[int]
    run_version: Optional[int]
    sandbox: Optional[JobSandbox]
    schedselect: Optional[str]
    security_context: Optional[str]
    server: Optional[str]
    session_id: Optional[int]
    shell_path_list: Optional[str]
    stagein: Optional[str]
    stageout: Optional[str]
    stageout_status: Optional[int]
    stime: Optional[int]
    submit_arguments: Optional[str]
    substate: Optional[int]
    topjob_ineligible: Optional[bool]
    umask: Optional[int]
    user_list: Optional[str]
    variable_list: Optional[str]
