from typing import Union
from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class QueueObject(AlterableObject):
    object_type = "queue"
    object_model = Queue
    attribute_model = Queue

    data: Queue

    def stat(self, attributes=None) -> Queue | None:
        return super().stat(attributes)


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
