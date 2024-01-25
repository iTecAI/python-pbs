from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class NodeObject(AlterableObject):
    object_type = "node"
    object_model = Node
    attribute_model = Node


class NodeOperator(BaseObjectManager):
    object_type = "node"
    object_model = Node
    object_factory = NodeObject
