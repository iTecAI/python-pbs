from pytest import fixture
from python_pbs import connect
from dotenv import load_dotenv
import os

load_dotenv()


@fixture
def con():
    return connect()


@fixture
def options():
    return os.environ
