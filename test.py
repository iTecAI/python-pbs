import time
from python_pbs import PBS, JobAttribute
from python_pbs.pbs.models.job import JobKeepFiles
from python_pbs.util import *

pbs = PBS()
print(pbs.server.data)
print(pbs.queues.all[0].data)
print(pbs.nodes.all[0].data)
# print(stat_resource(pbs.connection, id="cput"))
