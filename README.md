# python-pbs
Modern python wrapper for OpenPBS

## Environment Setup
- The PBS libraries MUST be in `$LD_LIBRARY_PATH`. These generally live in `/opt/pbs/lib`, but that may vary depending on the system.

## Development
- Clone the github repository
- Run `poetry install` in the main directory

## Installation
The project is currently not on PyPi, so should be installed as follows:
```
python -m pip install git+https://github.com/iTecAI/python-pbs.git
```

This should install & build all the required dependencies.

## Basic Usage

```python
from python_pbs import PBS, JobAttribute

pbs = PBS() # Connects to default server
print(pbs.status) # Prints server details
print(pbs.jobs.select(criteria=[JobAttribute(name="job_owner", value="<your username>")])) # Returns all running jobs you own
print(pbs.queues["workq"].available("username")) # Returns number of qsubs available for user in workq
```
