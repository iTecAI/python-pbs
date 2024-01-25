from typing import Literal, Union
from ..models import Job
from python_pbs.util import stat_job


class JobObject:
    object_type = "job"
    object_model = Job
    attribute_model = Job

    def __init__(self, connection_id: int, data: Job) -> None:
        self.connection = connection_id
        self.data = data

    def stat(
        self, attributes: Job = Job, historical: bool = False, subjobs: bool = False
    ) -> Union[Job, None]:
        result = stat_job(
            self.connection,
            id=self.data.id,
            attributes=attributes.to_attributes() if attributes else [],
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
    ) -> list[Job]:
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
