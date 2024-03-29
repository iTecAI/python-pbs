import asyncio
from enum import Enum
import os
import time
from typing import Any, AsyncGenerator, Generator, Literal, Union
from python_pbs.pbs.exceptions import PBSException
from ..models import Job
from python_pbs.util import (
    stat_job,
    Attribute,
    select_jobs,
    delete_job,
    rerun_job,
    alter_job,
    hold_job,
    release_job,
    swap_jobs,
)


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


class JobOutputFile(Enum):
    OUTPUT = "OU"
    ERROR = "ER"


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

    def logs(
        self,
        spool_path="/var/spool/pbs/spool",
        file: JobOutputFile = JobOutputFile.OUTPUT,
        yield_waiting: bool = False,
    ) -> Generator[str, Any, Any]:
        with open(os.path.join(spool_path, f"{self.data.id}.{file.value}"), "r") as f:
            while True:
                if not os.path.exists(
                    os.path.join(spool_path, f"{self.data.id}.{file.value}")
                ):
                    break
                line = f.readline()
                if not line:
                    if yield_waiting:
                        yield None
                    time.sleep(0.1)
                    continue
                yield line

    async def logs_async(
        self,
        spool_path="/var/spool/pbs/spool",
        file: JobOutputFile = JobOutputFile.OUTPUT,
        yield_waiting: bool = False,
    ) -> AsyncGenerator[str, Any]:
        with open(os.path.join(spool_path, f"{self.data.id}.{file.value}"), "r") as f:
            while True:
                if not os.path.exists(
                    os.path.join(spool_path, f"{self.data.id}.{file.value}")
                ):
                    break
                line = f.readline()
                if not line:
                    if yield_waiting:
                        yield None
                    await asyncio.sleep(0.1)
                    continue
                yield line

    def delete(self) -> None:
        result = delete_job(self.connection, self.data.id)
        if result == 0:
            return None

        raise PBSException(result, context=f"Failed to delete job {self.data.id}")

    def rerun(self) -> None:
        result = rerun_job(self.connection, self.data.id)

        if result == 0:
            self.reload()
            return None

        raise PBSException(result, context=f"Failed to rerun job {self.data.id}")

    def set(self, attributes: list[JobAttribute]):
        result = alter_job(
            self.connection,
            self.data.id,
            JobAttribute.make_attrl(attributes, with_op=True),
        )
        if result == 0:
            self.reload()
        else:
            raise PBSException(
                code=result, context=f"Attempting to alter job {self.data.id}"
            )

    def hold(self, type: Literal["u", "o", "s"] = "u") -> None:
        result = hold_job(self.connection, self.data.id, hold_type=type)

        if result == 0:
            self.reload()
            return None

        raise PBSException(result, context=f"Failed to hold job {self.data.id}")

    def release(self, type: Literal["u", "o", "s"] = "u") -> None:
        result = release_job(self.connection, self.data.id, hold_type=type)

        if result == 0:
            self.reload()
            return None

        raise PBSException(result, context=f"Failed to release job {self.data.id}")

    def swap(self, other: Union[Job, "JobObject"]) -> None:
        if isinstance(other, Job):
            jid = other.id
        else:
            jid = other.data.id

        result = swap_jobs(self.connection, self.data.id, jid)
        if result == 0:
            self.reload()
            return None

        raise PBSException(
            result, context=f"Failed to swap job {self.data.id} with job {jid}"
        )


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
    def all(self) -> list[JobObject]:
        return self.stat()

    @property
    def all_complete(self) -> list[JobObject]:
        return self.stat(historical=True, subjobs=True)

    def get(
        self, id: str, historical: bool = False, subjob: bool = False
    ) -> Union[JobObject, None]:
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
