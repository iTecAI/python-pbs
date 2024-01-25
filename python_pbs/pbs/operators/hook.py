from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class HookObject(AlterableObject):
    object_type = "hook"
    object_model = Hook
    attribute_model = Hook


class HookOperator(BaseObjectManager):
    object_type = "hook"
    object_model = Hook
    object_factory = HookObject
