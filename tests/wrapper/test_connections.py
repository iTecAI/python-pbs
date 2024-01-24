from python_pbs import *


def test_connect(con: int):
    assert type(con) == int
    assert con >= 0


def test_connect_bad():
    c = connect(name="badserver")
    assert type(c) == int
    assert c < 0


def test_disconnect(con: int):
    assert type(con) == int
    assert con >= 0
    assert disconnect(con) == 0
