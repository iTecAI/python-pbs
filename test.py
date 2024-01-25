from python_pbs import PBS
from python_pbs.util import *

pbs = PBS()
"""print(pbs.status)
print(pbs.queues)
print(pbs.get_jobs(ids=["9.hulkling", "8.hulkling"], include_historical=True))"""

print(stat_node(pbs.connection))
