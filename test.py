from python_pbs import PBS
from python_pbs.util import *

pbs = PBS()
print(pbs.server.data)
pbs.server.set("job_history_enable", True)
