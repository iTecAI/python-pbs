from typing import Union
from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class NodeObject(AlterableObject):
    object_type = "node"
    object_model = Node
    attribute_model = Node

    data: Node

    def stat(self, attributes=None) -> Node | None:
        return super().stat(attributes)


class NodeOperator(BaseObjectManager):
    object_type = "node"
    object_model = Node
    object_factory = NodeObject

    @property
    def all(self) -> list[NodeObject]:
        return super().all

    def get(self, id: str) -> NodeObject | None:
        return super().get(id)

    def __getitem__(self, key) -> NodeObject:
        return super().__getitem__(key)
