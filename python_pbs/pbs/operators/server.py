from typing import Union
from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class ServerObject(AlterableObject):
    object_type = "server"
    object_model = Server
    attribute_model = Server

    data: Server

    def stat(self, attributes=None) -> Server | None:
        return super().stat(attributes)


class ServerOperator(BaseObjectManager):
    object_type = "server"
    object_model = Server
    object_factory = ServerObject

    @property
    def all(self) -> list[ServerObject]:
        return super().all

    def get(self, id: str) -> ServerObject | None:
        return super().get(id)

    def __getitem__(self, key) -> ServerObject:
        return super().__getitem__(key)
