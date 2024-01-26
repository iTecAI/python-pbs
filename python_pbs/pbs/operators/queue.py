from enum import Enum
from typing import Union

from matplotlib.style import available

from ...util.typed_wrapper import BatchOperation
from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *
from python_pbs.util import select_jobs, Attribute, stat_job


class QueueObject(AlterableObject):
    object_type = "queue"
    object_model = Queue
    attribute_model = Queue

    data: Queue

    def stat(self, attributes=None) -> Queue | None:
        return super().stat(attributes)

    def can_access(self, user: str) -> bool:
        if not self.data.acl_user_enable:
            return True

        return user in self.data.acl_users.split(",")

    def available(self, user: str) -> int:
        if not self.can_access(user):
            return 0

        if not self.data.resources_available.get("ncpus"):
            return None

        ids = select_jobs(
            self.connection, [Attribute(name="queue", value=self.data.id)]
        )
        jobs = [
            Job.from_pbs(i)
            for i in stat_job(self.connection, id=",".join(ids))
            if i.get("Job_Owner", "").startswith(user + "@")
        ]

        cpu_usage = sum(
            [
                i.resources_used.get("ncpus", None) if i.resources_used else None
                for i in jobs
            ]
        )

        queue_max = self.data.resources_available.get("ncpus")
        queue_assigned = self.data.resources_assigned.get("ncpus", 0)
        queue_availability = max(0, queue_max - queue_assigned)
        max_user_cpus = self.data.max_user_res.get("ncpus", queue_availability)
        user_available = max_user_cpus - cpu_usage

        if user_available > queue_availability:
            avaliable = queue_availability
        else:
            available = user_available

        if available > max_user_cpus:
            avaliable = max_user_cpus

        if available > 0 and self.data.default_chunk.get("ncpus"):
            available -= available % self.data.default_chunk.get("ncpus")

        return max(0, available)


class QueueOperator(BaseObjectManager):
    object_type = "queue"
    object_model = Queue
    object_factory = QueueObject

    @property
    def all(self) -> list[QueueObject]:
        return super().all

    def get(self, id: str) -> QueueObject | None:
        return super().get(id)

    def __getitem__(self, key) -> QueueObject:
        return super().__getitem__(key)
