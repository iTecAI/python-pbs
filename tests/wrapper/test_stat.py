from python_pbs.util.typed_wrapper import *


def test_stat_queues(con: int, options: dict):
    result = stat_queue(con)
    assert type(result) == list
    assert type(result[0]) == dict
    assert result[0]["id"] == options["OPTION_QUEUE_ID"]
    assert result[0]["enabled"] == "True"


def test_stat_jobs(con: int):
    result = stat_job(con)
    assert type(result) == list


def test_stat_node(con: int, options: dict):
    result = stat_node(con)
    assert type(result) == list
    assert type(result[0]) == dict
    assert result[0]["id"] == options["OPTION_NODE_ID"]


def test_stat_server(con: int, options: dict):
    result = stat_server(con)
    assert type(result) == list
    assert type(result[0]) == dict
    assert result[0]["id"] == options["OPTION_SERVER_ID"]


def test_stat_resource(con: int):
    result = stat_resource(con)
    assert type(result) == list
    assert all([type(i) == dict for i in result])
    ids = [i["id"] for i in result]
    assert "cput" in ids
    assert "mem" in ids
    assert "arch" in ids


def test_specific_resource(con: int):
    result = stat_resource(con, id="cput")
    assert type(result) == list
