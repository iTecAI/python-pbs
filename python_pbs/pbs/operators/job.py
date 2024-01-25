from typing import Literal, Union
from ..models import Job
from python_pbs.util import stat_job, Attribute, select_jobs


class JobAttribute(Attribute):
    name: Literal[
        "account_name",
        "accounting_id",
        "accrue_type",
        "alt_id",
        "argument_list",
        "array",
        "array_id",
        "array_index",
        "array_indices_remaining",
        "array_indices_submitted",
        "array_state_count",
        "block",
        "checkpoint",
        "comment",
        "create_resv_from_job",
        "ctime",
        "depend",
        "egroup",
        "eligible_time",
        "error_path",
        "estimated",
        "etime",
        "euser",
        "execution_time",
        "exec_host",
        "exec_vnode",
        "exit_status",
        "forward_x11_cookie",
        "forward_x11_port",
        "group_list",
        "hold_types",
        "interactive",
        "jobdir",
        "job_name",
        "job_owner",
        "job_state",
        "join_path",
        "keep_files",
        "mail_points",
        "mail_users",
        "max_run_subjobs",
        "mtime",
        "output_path",
        "pcap_accelerator",
        "pcap_node",
        "pgov",
        "priority",
        "project",
        "pstate",
        "qtime",
        "queue",
        "queue_rank",
        "queue_type",
        "release_nodes_on_stageout",
        "remove_files",
        "rerunable",
        "resource_list",
        "resources_released",
        "resource_release_list",
        "resources_used",
        "run_count",
        "run_version",
        "sandbox",
        "schedselect",
        "security_context",
        "server",
        "session_id",
        "shell_path_list",
        "stagein",
        "stageout",
        "stageout_status",
        "stime",
        "submit_arguments",
        "substate",
        "topjob_ineligible",
        "umask",
        "user_list",
        "variable_list",
    ]


class JobObject:
    object_type = "job"
    object_model = Job
    attribute_model = JobAttribute

    def __init__(self, connection_id: int, data: Job) -> None:
        self.connection = connection_id
        self.data = data

    def stat(
        self,
        attributes: list[JobAttribute] = None,
        historical: bool = False,
        subjobs: bool = False,
    ) -> Union[Job, None]:
        result = stat_job(
            self.connection,
            id=self.data.id,
            attributes=JobAttribute.make_attrl(attributes) if attributes else None,
            historical=historical,
            subjobs=subjobs,
        )
        if len(result) > 0:
            return Job.from_pbs(result[0])
        else:
            return None

    def reload(self) -> None:
        result = self.stat()
        if result:
            self.data = result


class JobOperator:
    object_type = "job"
    object_model = Job
    object_factory = JobObject

    def __init__(self, connection: int):
        self.connection = connection

    def stat(
        self, ids: list[str] = None, historical: bool = False, subjobs: bool = False
    ) -> list[JobObject]:
        result = stat_job(
            self.connection,
            id=",".join(ids) if ids else None,
            historical=historical,
            subjobs=subjobs,
        )
        return [
            self.object_factory(self.connection, self.object_model.from_pbs(i))
            for i in result
        ]

    @property
    def all(self) -> list[Job]:
        return self.stat()

    @property
    def all_complete(self) -> list[Job]:
        return self.stat(historical=True, subjobs=True)

    def get(
        self, id: str, historical: bool = False, subjob: bool = False
    ) -> Union[Job, None]:
        result = self.stat(ids=[id], historical=historical, subjobs=subjob)
        if len(result) > 0:
            return result[0]
        else:
            fallback = {
                i["id"]: i
                for i in stat_job(
                    self.connection, historical=historical, subjobs=subjob
                )
            }
            if id in fallback.keys():
                return self.object_factory(
                    self.connection, self.object_model.from_pbs(fallback[id])
                )
            else:
                return None

    def __getitem__(self, key) -> Job:
        result = self.get(key, historical=True, subjob=True)
        if not result:
            raise KeyError(f"{key} is not a known {self.object_type} name.")

        return result

    def select(
        self,
        criteria: list[JobAttribute] = None,
        include_historical: bool = False,
        include_subjobs: bool = False,
    ) -> list[JobObject]:
        ids = select_jobs(
            self.connection,
            criteria,
            historical=include_historical,
            subjobs=include_subjobs,
        )
        if len(ids) == 0:
            return []
        return self.stat(
            ids=ids, historical=include_historical, subjobs=include_subjobs
        )
