from typing import Union
from ..util import *
from .exceptions import PBSException
from .models import *


class PBS:
    def __init__(self, server: Union[str, None] = None) -> None:
        self.server_name = server if server else default_server()
        self.connection = connect(self.server_name)
        if self.connection < 0:
            raise PBSException(abs(self.connection), context="Connection attempt")

    @property
    def status(self) -> Server:
        return Server.from_pbs(stat_server(self.connection)[0])

    @property
    def queues(self) -> list[Queue]:
        return [Queue.from_pbs(i) for i in stat_queue(self.connection)]

    def get_queue(self, id: str) -> Union[Queue, None]:
        result = stat_queue(self.connection, id=id)
        if len(result) > 0:
            return Queue.from_pbs(result[0])
        else:
            return None

    def get_jobs(
        self,
        ids: Union[str, list[str]] = None,
        include_historical: bool = False,
        include_subjobs: bool = False,
    ) -> list[Job]:
        if type(ids) == list:
            ids = ",".join(ids)

        result = stat_job(
            self.connection,
            id=ids,
            historical=include_historical,
            subjobs=include_subjobs,
        )

        return [Job.from_pbs(i) for i in result]
