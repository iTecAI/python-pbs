import time
from python_pbs import PBS, JobAttribute
from python_pbs.pbs.models.job import JobKeepFiles
from python_pbs.util import *

pbs = PBS()
print(pbs.server.data)
# print(pbs.queues["s1"].available("dharr"))
pbs.submit_script(
    "test_script.sh", output_directory="test-out/curl-test", alt_user="dharr"
)
