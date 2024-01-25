from pytest import fixture
from python_pbs.util.typed_wrapper import *
from dotenv import load_dotenv
import os

load_dotenv()


@fixture
def con():
    return connect(os.environ["OPTION_SERVER_ID"])


@fixture
def options():
    return os.environ
