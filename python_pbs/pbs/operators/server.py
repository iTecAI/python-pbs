from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class ServerObject(AlterableObject):
    object_type = "server"
    object_model = Server
    attribute_model = Server


class ServerOperator(BaseObjectManager):
    object_type = "server"
    object_model = Server
    object_factory = ServerObject
