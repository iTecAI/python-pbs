from typing import Union
from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class SchedulerObject(AlterableObject):
    object_type = "scheduler"
    object_model = Scheduler
    attribute_model = Scheduler

    data: Scheduler

    def stat(self, attributes=None) -> Scheduler | None:
        return super().stat(attributes)


class SchedulerOperator(BaseObjectManager):
    object_type = "scheduler"
    object_model = Scheduler
    object_factory = SchedulerObject

    @property
    def all(self) -> list[SchedulerObject]:
        return super().all

    def get(self, id: str) -> SchedulerObject | None:
        return super().get(id)

    def __getitem__(self, key) -> SchedulerObject:
        return super().__getitem__(key)
