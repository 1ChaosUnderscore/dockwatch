import time

from rich.live import Live
from rich.table import Table

import docker_client

def createTable():
    table = Table()

    #Every container uses this
    table.add_column("Container")
    table.add_column("CPU %")
    table.add_column("RAM %")
    table.add_column("Network I/O")

    for i in docker_client.containers:
        table.add_row(i.name)
    
    return table

with Live(createTable(), refresh_per_second=2) as live:
    while True:
        time.sleep(0.5)
        live.update(createTable())