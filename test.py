from python_pbs import PBS

pbs = PBS()
print(pbs.status)
print(pbs.queues)
print(pbs.get_jobs(ids=["9.hulkling", "8.hulkling"], include_historical=True))
