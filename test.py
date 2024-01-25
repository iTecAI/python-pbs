from python_pbs import PBS, JobAttribute
from python_pbs.util import *

pbs = PBS()
print(pbs.server.data)
print(pbs.queues["workq"].data)
print(pbs.nodes["hulkling"].data)
print(pbs.schedulers["default"].data)
print(
    pbs.jobs.select(
        criteria=[JobAttribute(name="job_state", value="F")], include_historical=True
    )[0].data
)
