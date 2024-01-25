from python_pbs import PBS
from python_pbs.util import *

pbs = PBS()
print(pbs.server.data)
print(pbs.queues["workq"].data)
print(pbs.nodes["hulkling"].data)
print(pbs.schedulers["default"].data)
print(pbs.jobs.all_complete[0].data)
