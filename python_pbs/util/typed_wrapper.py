from typing import Literal, Optional, Union
from ..extensions import *
from pydantic import BaseModel
from enum import Enum


class ManagerCommand(Enum):
    NONE = MGR_CMD_NONE
    CREATE = MGR_CMD_CREATE
    DELETE = MGR_CMD_DELETE
    SET = MGR_CMD_SET
    UNSET = MGR_CMD_UNSET
    LIST = MGR_CMD_LIST
    PRINT = MGR_CMD_PRINT
    ACTIVE = MGR_CMD_ACTIVE
    IMPORT = MGR_CMD_IMPORT
    EXPORT = MGR_CMD_EXPORT
    LAST = MGR_CMD_LAST


class ManagerObject(Enum):
    NONE = MGR_OBJ_NONE
    SERVER = MGR_OBJ_SERVER
    QUEUE = MGR_OBJ_QUEUE
    JOB = MGR_OBJ_JOB
    NODE = MGR_OBJ_NODE
    RESERVATION = MGR_OBJ_RESV
    RESOURCE = MGR_OBJ_RSC
    SCHEDULER = MGR_OBJ_SCHED
    HOST = MGR_OBJ_HOST
    HOOK = MGR_OBJ_HOOK
    PBS_HOOK = MGR_OBJ_PBS_HOOK
    JOB_ARRAY_PARENT = MGR_OBJ_JOBARRAY_PARENT
    SUB_JOB = MGR_OBJ_SUBJOB
    LAST = MGR_OBJ_LAST


class BatchOperation(Enum):
    SET = SET
    UNSET = UNSET
    INCR = INCR
    DECR = DECR
    EQ = EQ
    NE = NE
    GE = GE
    GT = GT
    LE = LE
    LT = LT
    DFLT = DFLT
    INTERNAL = INTERNAL


class MessageFile(Enum):
    OUT = MSG_OUT
    ERROR = MSG_ERR


class TerminationMode(Enum):
    IMMEDIATE = SHUT_IMMEDIATE
    DELAYED = SHUT_DELAY
    QUICK = SHUT_QUICK


class Attribute(BaseModel):
    name: str
    resource: Optional[str] = None
    value: Optional[str] = None
    operation: Optional[BatchOperation] = None

    @staticmethod
    def make_attrl(
        attributes: list["Attribute"], with_op: bool = False
    ) -> Union[attrl, attropl]:
        if len(attributes) == 0:
            return None

        root = attropl() if with_op else attrl()
        current = root
        count = 1
        for i in attributes:
            current.name = i.name
            current.resource = i.resource
            current.value = i.value
            if with_op:
                current.op = (
                    i.operation.value if i.operation else BatchOperation.EQ.value
                )
            if count < len(attributes):
                current.next = attropl() if with_op else attrl()
                current = current.next
            count += 1

        return root

    @classmethod
    def from_attrl(cls, attr: attrl) -> list["Attribute"]:
        results = []
        current = attr
        while current:
            results.append(
                Attribute(
                    name=current.name,
                    resource=current.resource,
                    value=current.value,
                    operation=current.op,
                )
            )
            current = current.next

        return results


class ResourceResult(BaseModel):
    successful: bool
    available: Optional[int] = None
    allocated: Optional[int] = None
    reserved: Optional[int] = None
    down: Optional[int] = None


class BatchStatus(BaseModel):
    name: str
    text: str
    attributes: list[Attribute]

    @staticmethod
    def make_batch_status(statuses: list["BatchStatus"]) -> batch_status:
        if len(statuses) == 0:
            return None

        root = batch_status()
        current = root
        count = 1
        for i in statuses:
            current.name = i.name
            current.text = i.text
            current.attribs = Attribute.make_attrl(i.attributes)
            if count < len(statuses):
                current.next = batch_status()
                current = current.next
            count += 1

        return root

    @classmethod
    def from_batch_status(cls, status: batch_status) -> list["BatchStatus"]:
        results = []
        current = status
        while current:
            results.append(
                BatchStatus(
                    name=current.name,
                    text=current.text,
                    attributes=Attribute.from_attrl(current.attribs),
                )
            )
            current = current.next

        return results


def connect(name: Union[str, None] = None) -> int:
    """Connect to PBS server

    Args:
        name (Union[str, None], optional): Server name. Defaults to None.

    Returns:
        int: Connection ID, or < 0 if error.
    """
    return pbs_connect(name)


def run_asynchronous_job(
    connection_id: int, job_id: str, location: Union[str, None] = None
) -> int:
    """An "Asynchronous Run Job" request is generated and sent to the server over the connection.
    The server will validate the request and reply before initiating the execution of the job. This version of the call can be used to reduce latency in scheduling, especially when the scheduler must start a large number of jobs.

    Args:
        connection_id (int): COnnection ID
        job_id (str): Job ID to be run, in the form `sequence_number.server`
        location (Union[str, None], optional): The location where the job should be run. Defaults to None.

    Returns:
        int: Result code (!= 0 is error)
    """
    return pbs_asyrunjob(connection_id, job_id, location, None)


def alter_job(connection_id: int, job_id: str, attributes: list[Attribute] = []):
    """Alters a job given an array of attributes

    Args:
        connection_id (int): Connection ID
        job_id (str): Job ID
        attributes (list[Attribute], optional): List of attributes to set. Defaults to [].

    Returns:
        _type_: _description_
    """
    return pbs_alterjob(
        connection_id, job_id, Attribute.make_attrl(attributes, with_op=True), None
    )


def default_server() -> str:
    """Gets the name of the default server

    Returns:
        str: Default server name
    """
    return pbs_default()


def delete_job(connection_id: int, job_id: str) -> int:
    """Deletes a job

    Args:
        connection_id (int): Connection ID
        job_id (int): Job ID

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_deljob(connection_id, job_id, None)


def disconnect(connection_id: int) -> int:
    """Disconnect from given connection

    Args:
        connection_id (int): Connection ID

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_disconnect(connection_id)


def hold_job(
    connection_id: int, job_id: str, hold_type: Literal["u", "o", "s"] = "u"
) -> int:
    """Hold a given job

    Args:
        connection_id (int): Connection ID
        job_id (str): Job ID
        hold_type (Literal[&quot;u&quot;, &quot;o&quot;, &quot;s&quot;], optional): Hold Type (see documentation). Defaults to "u".

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_holdjob(connection_id, job_id, hold_type, None)


def locate_job(connection_id: int, job_id: str) -> Union[str, None]:
    """Locates a given job

    Args:
        connection_id (int): Connection ID
        job_id (str): Job ID

    Returns:
        Union[str, None]: Location or None if error
    """
    return pbs_locjob(connection_id, job_id, None)


def execute_manager_command(
    connection_id: int,
    command: ManagerCommand,
    object: ManagerObject,
    object_name: str,
    attributes: list[Attribute],
) -> int:
    """Executes a qmgr command on the given connection

    Args:
        connection_id (int): Connection ID
        command (ManagerCommand): Command
        object (ManagerObject): Object type
        object_name (str): Object name
        attributes (list[Attribute]): Attributes (should include names, values, ops)

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_manager(
        connection_id,
        command.value,
        object.value,
        object_name,
        Attribute.make_attrl(attributes, with_op=True),
        None,
    )


def move_job(connection_id: int, job_id: str, destination: Optional[str] = None) -> int:
    """Moves a job to a new destination

    Args:
        connection_id (int): Connection ID
        job_id (str): Job ID
        destination (Optional[str], optional): Destination, default if None. Defaults to None.

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_movejob(connection_id, job_id, destination, None)


def message_job(
    connection_id: int, job_id: str, file: MessageFile, message: str
) -> int:
    """Sends a message to the output file of a job

    Args:
        connection_id (int): Connection ID
        job_id (str): Job ID
        file (MessageFile): Which file to send to
        message (str): Message to send

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_msgjob(connection_id, job_id, file, message, None)


def swap_jobs(connection_id: int, job_id_1: str, job_id_2: str) -> int:
    """Swaps the order of two jobs in the queue

    Args:
        connection_id (int): Connection ID
        job_id_1 (str): Job ID
        job_id_2 (str): Job ID

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_orderjob(connection_id, job_id_1, job_id_2, None)


def rerun_job(connection_id: int, job_id: str) -> int:
    """Rerun a given job

    Args:
        connection_id (int): Connection ID
        job_id (str): Job ID
    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_rerunjob(connection_id, job_id, None)


def run_job(connection_id: int, job_id: str, location: Optional[str] = None) -> int:
    """Runs a given job

    Args:
        connection_id (int): Connection ID
        job_id (str): Job ID
        location (Optional[str], optional): Location to run at. Defaults to None.

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_runjob(connection_id, job_id, location, None)


def select_jobs(connection_id: int, attributes: list[Attribute]) -> list[str]:
    """Select jobs based on criteria

    Args:
        connection_id (int): Connection ID
        attributes (list[Attribute]): Attributes to match

    Returns:
        list[str]: List of results
    """
    result = pbs_selectjob(
        connection_id, Attribute.make_attrl(attributes, with_op=True), None
    )
    return [] if result == None else result


def signal_job(connection_id: int, job_id: str, signal: str) -> int:
    """Sends an OS signal to the job

    Args:
        connection_id (int): Connection ID
        job_id (str): Job ID
        signal (str): Signal to send

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_sigjob(connection_id, job_id, signal, None)


def stat_free(status: list[BatchStatus]) -> None:
    """Free space held by stat functions

    Args:
        status (list[BatchStatus]): List of statuses to free
    """
    pbs_statfree(BatchStatus.make_batch_status(status))


def stat_job(
    connection_id: int, id: Optional[str] = "", attributes: list[Attribute] = [], historical: bool = False, subjobs: bool = False
) -> list[dict]:
    """Get status of job(s)

    Args:
        connection_id (int): Connection ID
        id (Optional[str], optional): Object ID or blank for all. Defaults to "".
        attributes (list[Attribute], optional): List of filter attributes. Defaults to None.

    Returns:
        list[dict]: List of statuses
    """
    return pbs_statjob(connection_id, id, Attribute.make_attrl(attributes), f"{'x' if historical else ''}{'t' if subjobs else ''}")


def stat_node(
    connection_id: int, id: Optional[str] = "", attributes: list[Attribute] = []
) -> list[dict]:
    """Get status of nodes(s)

    Args:
        connection_id (int): Connection ID
        id (Optional[str], optional): Object ID or blank for all. Defaults to "".
        attributes (list[Attribute], optional): List of filter attributes. Defaults to None.

    Returns:
        list[dict]: List of statuses
    """
    return pbs_statnode(connection_id, id, Attribute.make_attrl(attributes), None)


def stat_queue(
    connection_id: int, id: Optional[str] = "", attributes: list[Attribute] = []
) -> list[dict]:
    """Get status of queue(s)

    Args:
        connection_id (int): Connection ID
        id (Optional[str], optional): Object ID or blank for all. Defaults to "".
        attributes (list[Attribute], optional): List of filter attributes. Defaults to None.

    Returns:
        list[dict]: List of statuses
    """
    return pbs_statque(connection_id, id, Attribute.make_attrl(attributes), None)


def stat_server(connection_id: int, attributes: list[Attribute] = []) -> list[dict]:
    """Get status of server

    Args:
        connection_id (int): Connection ID
        attributes (list[Attribute], optional): List of filter attributes. Defaults to None.

    Returns:
        list[dict]: Server status
    """
    return pbs_statserver(connection_id, Attribute.make_attrl(attributes), None)


def stat_resource(
    connection_id: int, id: Optional[str] = "", attributes: list[Attribute] = []
) -> list[dict]:
    """Get status of resource(s)

    Args:
        connection_id (int): Connection ID
        id (Optional[str], optional): Object ID or blank for all. Defaults to "".
        attributes (list[Attribute], optional): List of filter attributes. Defaults to None.

    Returns:
        list[dict]: List of statuses
    """
    return pbs_statrsc(connection_id, id, Attribute.make_attrl(attributes), None)


def stat_scheduler(connection_id: int, attributes: list[Attribute] = []) -> list[dict]:
    """Get status of scheduler

    Args:
        connection_id (int): Connection ID
        attributes (list[Attribute], optional): List of filter attributes. Defaults to None.

    Returns:
        list[dict]: Scheduler status
    """
    return pbs_statsched(connection_id, Attribute.make_attrl(attributes), None)


def stat_reservation(
    connection_id: int, id: Optional[str] = "", attributes: list[Attribute] = []
) -> list[dict]:
    """Get status of reservation(s)

    Args:
        connection_id (int): Connection ID
        id (Optional[str], optional): Object ID or blank for all. Defaults to "".
        attributes (list[Attribute], optional): List of filter attributes. Defaults to None.

    Returns:
        list[dict]: List of statuses
    """
    return pbs_statresv(connection_id, id, Attribute.make_attrl(attributes), None)


def stat_hook(
    connection_id: int, id: Optional[str] = "", attributes: list[Attribute] = []
) -> list[dict]:
    """Get status of hook(s)

    Args:
        connection_id (int): Connection ID
        id (Optional[str], optional): Object ID or blank for all. Defaults to "".
        attributes (list[Attribute], optional): List of filter attributes. Defaults to None.

    Returns:
        list[dict]: List of statuses
    """
    return pbs_stathook(connection_id, id, Attribute.make_attrl(attributes), None)


def submit_job(
    connection_id: int,
    attributes: list[Attribute],
    script: str,
    destination: Optional[str] = None,
) -> str:
    """Submits a job to PBS

    Args:
        connection_id (int): Connection ID
        attributes (list[Attribute]): Attributes
        script (str): Script path
        destination (Optional[str], optional): Destination. Defaults to None.

    Returns:
        str: Created job ID
    """
    return pbs_submit(
        connection_id,
        Attribute.make_attrl(attributes, with_op=True),
        script,
        destination,
        None,
    )


def terminate(connection_id: int, manner: TerminationMode) -> int:
    """Terminate batch server

    Args:
        connection_id (int): Connection ID
        manner (TerminationMode): How to shut down

    Returns:
        int: 0 if successful, otherwise error
    """
    return pbs_terminate(connection_id, manner, None)
