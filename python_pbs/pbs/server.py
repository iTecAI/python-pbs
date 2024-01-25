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
