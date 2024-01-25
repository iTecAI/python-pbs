from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class QueueObject(AlterableObject):
    object_type = "queue"
    object_model = Queue
    attribute_model = Queue


class QueueOperator(BaseObjectManager):
    object_type = "queue"
    object_model = Queue
    object_factory = QueueObject
