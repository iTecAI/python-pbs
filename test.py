from python_pbs import connect, stat_queue, stat_server

c = connect()
print(stat_queue(c))
print(stat_server(c))
