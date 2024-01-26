import os
from typing import Union
from ..util import *
from .exceptions import PBSException
from .models import *
from .operators import *


class PBS:
    def __init__(self, server: Union[str, None] = None) -> None:
        """Primary wrapper class for the PBS API

        :param server: Server name or None for default, defaults to None
        :type server: Union[str, None], optional
        :raises PBSException: Failed connection
        """
        self.server_name = server if server else default_server()
        self.connection = connect(self.server_name)
        if self.connection < 0:
            raise PBSException(abs(self.connection), context="Connection attempt")

    @property
    def server(self) -> ServerObject:
        """Get the server Object currently connected

        :return: Server object
        :rtype: ServerObject
        """
        return ServerOperator(self.connection).get(self.server_name)

    @property
    def status(self) -> Server:
        """Utility property to get server status directly

        :return: Server model
        :rtype: Server
        """
        return ServerOperator(self.connection).get(self.server_name).data

    @property
    def hooks(self) -> HookOperator:
        """Gets the HookOperator

        :return: HookOperator object
        :rtype: HookOperator
        """
        return HookOperator(self.connection)

    @property
    def nodes(self) -> NodeOperator:
        """Gets the NodeOperator

        :return: NodeOperator object
        :rtype: NodeOperator
        """
        return NodeOperator(self.connection)

    @property
    def queues(self) -> QueueOperator:
        """Gets the QueueOperator

        :return: QueueOperator object
        :rtype: QueueOperator
        """
        return QueueOperator(self.connection)

    @property
    def schedulers(self) -> SchedulerOperator:
        """Gets the SchedulerOperator

        :return: SchedulerOperator object
        :rtype: SchedulerOperator
        """
        return SchedulerOperator(self.connection)

    @property
    def jobs(self) -> JobOperator:
        """Gets the JobOperator object

        :return: JobOperator object
        :rtype: JobOperator
        """
        return JobOperator(self.connection)

    def submit_script(
        self,
        script: str,
        queue: str = None,
        name: str = None,
        attributes: JobSubmission = {},
        output_directory: str = None,
    ) -> JobObject:
        """Submits a script job (ie, a shell file) and returns its status

        :param script: Path to script file
        :type script: str
        :param queue: Queue name, defaults to None
        :type queue: str, optional
        :param name: Job name, defaults to None
        :type name: str, optional
        :param attributes: Attribute mapping, defaults to {}
        :type attributes: JobSubmission, optional
        :param output_directory: Output folder path, defaults to None
        :type output_directory: str, optional
        :raises PBSException: If job failed to submit
        :return: Initialized job
        :rtype: JobObject
        """
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)
            attributes["output_path"] = os.path.join(
                os.path.abspath(output_directory),
                f"{name}.out.log" if name else "script.out.log",
            )
            attributes["error_path"] = os.path.join(
                os.path.abspath(output_directory),
                f"{name}.err.log" if name else "script.err.log",
            )
        if name:
            attributes["job_name"] = name
        parsed_attrs = [
            Attribute(name=k, value=v, operation=BatchOperation.SET)
            for k, v in attributes.items()
        ]
        result = submit_job(self.connection, parsed_attrs, script, destination=queue)
        if result == None:
            raise PBSException(-1, context="Job submission failed.")
        else:
            return self.jobs.get(result, historical=True, subjob=True)

    def submit_command(
        self,
        executable: str,
        *args,
        queue: str = None,
        name: str = None,
        attributes: JobSubmission = {},
        output_directory: str = None,
    ) -> JobObject:
        """Submit a command directly to PBS (ie from STDIN)

        :param executable: Executable path
        :type executable: str
        :param *args: List of arguments
        :type *args: list[str]
        :param queue: Queue name, defaults to None
        :type queue: str, optional
        :param name: Job name, defaults to None
        :type name: str, optional
        :param attributes: Attribute mapping, defaults to {}
        :type attributes: JobSubmission, optional
        :param output_directory: Output folder path, defaults to None
        :type output_directory: str, optional
        :raises PBSException: If job failed to submit
        :return: Initialized job
        :rtype: JobObject
        """
        if output_directory:
            os.makedirs(output_directory, exist_ok=True)
            attributes["output_path"] = os.path.join(
                os.path.abspath(output_directory),
                f"{name}.out.log" if name else "script.out.log",
            )
            attributes["error_path"] = os.path.join(
                os.path.abspath(output_directory),
                f"{name}.err.log" if name else "script.err.log",
            )
        if name:
            attributes["job_name"] = name
        attributes[
            "executable"
        ] = f"<jsdl-hpcpa:Executable>{executable}</jsdl-hpcpa:Executable>"
        attributes["argument_list"] = (
            " ".join([f"<jsdl-hpcpa:Argument>{i}</jsdl-hpcpa:Argument>" for i in args])
            if len(args) > 0
            else None
        )
        parsed_attrs = [
            Attribute(name=k, value=v, operation=BatchOperation.SET)
            for k, v in attributes.items()
        ]
        result = submit_job(self.connection, parsed_attrs, None, destination=queue)
        if result == None:
            raise PBSException(-1, context="Job submission failed.")
        else:
            return self.jobs.get(result, historical=True, subjob=True)
