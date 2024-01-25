from typing import Any, Literal, TypeVar, Union

from pydantic import BaseModel
from python_pbs.util import (
    stat_hook,
    stat_node,
    stat_queue,
    stat_scheduler,
    stat_server,
    Attribute,
    BatchOperation,
    execute_manager_command,
    ManagerCommand,
    ManagerObject,
)

stat_map = {
    "hook": stat_hook,
    "node": stat_node,
    "queue": stat_queue,
    "scheduler": stat_scheduler,
    "server": stat_server,
}

object_map = {
    "hook": ManagerObject.HOOK,
    "node": ManagerObject.NODE,
    "queue": ManagerObject.QUEUE,
    "scheduler": ManagerObject.SCHEDULER,
    "server": ManagerObject.SERVER,
}


class BaseAttributeModel(BaseModel):
    def to_attributes(self) -> list[Attribute]:
        return [Attribute(name=k, value=str(v)) for k, v in self.model_dump().items()]


M = TypeVar("M", BaseModel, None)
A = TypeVar("A", BaseAttributeModel, None)


class BaseObject:
    object_type: Literal["hook", "node", "queue", "scheduler", "server"]
    object_model: M
    attribute_model: A

    def __init__(self, connection_id: int, data: M) -> None:
        self.connection = connection_id
        self.data = data

    def stat(self, attributes: A = None) -> Union[M, None]:
        result = stat_map[self.object_type](
            self.connection,
            id=self.data.id,
            attributes=attributes.to_attributes() if attributes else [],
        )
        if len(result) > 0:
            return self.object_model.from_pbs(result[0])
        else:
            return None

    def reload(self) -> None:
        result = self.stat()
        if result:
            self.data = result


class AlterableObject(BaseObject):
    def set(
        self, property: str, value: Any, operation: BatchOperation = BatchOperation.EQ
    ):
        result = execute_manager_command(
            self.connection,
            ManagerCommand.SET,
            object_map[self.object_type],
            self.data.id,
            [Attribute(name=property, value=str(value), operation=operation)],
        )
        print(result)
        self.reload()


O = TypeVar("O", BaseObject, None)


class BaseObjectManager:
    object_type: Literal["hook", "node", "queue", "scheduler", "server"]
    object_model: M
    object_factory: O

    def __init__(self, connection: int):
        self.connection = connection

    def stat(self, ids: list[str] = None) -> list[O]:
        result = stat_map[self.object_type](
            self.connection, id=",".join(ids) if ids else None
        )
        return [
            self.object_factory(self.connection, self.object_model.from_pbs(i))
            for i in result
        ]

    @property
    def all(self) -> list[O]:
        return self.stat()

    def get(self, id: str) -> Union[O, None]:
        result = self.stat(ids=[id])
        if len(result) > 0:
            return result[0]
        else:
            fallback = {i["id"]: i for i in stat_map[self.object_type](self.connection)}
            if id in fallback.keys():
                return self.object_factory(
                    self.connection, self.object_model.from_pbs(fallback[id])
                )
            else:
                return None

    def __getitem__(self, key) -> O:
        result = self.get(key)
        if not result:
            raise KeyError(f"{key} is not a known {self.object_type} name.")

        return result
