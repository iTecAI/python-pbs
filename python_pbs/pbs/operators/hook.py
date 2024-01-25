from typing import Union
from .base import BaseAttributeModel, BaseObject, BaseObjectManager, AlterableObject
from ..models import *


class HookObject(AlterableObject):
    object_type = "hook"
    object_model = Hook
    attribute_model = Hook

    data: Hook

    def stat(self, attributes=None) -> Hook | None:
        return super().stat(attributes)


class HookOperator(BaseObjectManager):
    object_type = "hook"
    object_model = Hook
    object_factory = HookObject

    @property
    def all(self) -> list[HookObject]:
        return super().all

    def get(self, id: str) -> HookObject | None:
        return super().get(id)

    def __getitem__(self, key) -> HookObject:
        return super().__getitem__(key)
