from python_pbs import PBS, JobAttribute
from python_pbs.pbs.models.job import JobKeepFiles
from python_pbs.util import *

pbs = PBS()
"""print(pbs.server.data)
print(pbs.queues["workq"].data)
print(pbs.nodes["hulkling"].data)
print(pbs.schedulers["default"].data)
print(
    pbs.jobs.select(
        criteria=[JobAttribute(name="job_state", value="F")], include_historical=True
    )[0].data
)"""
result = pbs.submit_script(
    "test_script.sh",
    queue="workq",
    name="curl-test",
    output_directory="./test-out/curl-test",
)
if result:
    print(result.data)
