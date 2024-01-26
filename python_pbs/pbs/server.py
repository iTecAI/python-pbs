from typing import Union
from ..util import *
from .exceptions import PBSException
from .models import *
from .operators import *


class PBS:
    def __init__(self, server: Union[str, None] = None) -> None:
        self.server_name = server if server else default_server()
        self.connection = connect(self.server_name)
        if self.connection < 0:
            raise PBSException(abs(self.connection), context="Connection attempt")

    @property
    def server(self) -> ServerObject:
        return ServerOperator(self.connection).get(self.server_name)

    @property
    def status(self) -> Server:
        return ServerOperator(self.connection).get(self.server_name).data

    @property
    def hooks(self) -> HookOperator:
        return HookOperator(self.connection)

    @property
    def nodes(self) -> NodeOperator:
        return NodeOperator(self.connection)

    @property
    def queues(self) -> QueueOperator:
        return QueueOperator(self.connection)

    @property
    def schedulers(self) -> SchedulerOperator:
        return SchedulerOperator(self.connection)

    @property
    def jobs(self) -> JobOperator:
        return JobOperator(self.connection)

    def submit_script(
        self, script: str, queue: str = None, attributes: JobSubmission = {}
    ) -> JobObject:
        parsed_attrs = [
            Attribute(name=k, value=v, operation=BatchOperation.SET)
            for k, v in attributes.items()
        ]
        result = submit_job(self.connection, parsed_attrs, script, destination=queue)
        if result == None:
            raise PBSException(-1, context="Job submission failed.")
        else:
            return self.jobs.get(result, historical=True, subjob=True)
