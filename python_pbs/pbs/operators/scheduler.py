from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class SchedulerObject(AlterableObject):
    object_type = "scheduler"
    object_model = Scheduler
    attribute_model = Scheduler


class SchedulerOperator(BaseObjectManager):
    object_type = "scheduler"
    object_model = Scheduler
    object_factory = SchedulerObject
