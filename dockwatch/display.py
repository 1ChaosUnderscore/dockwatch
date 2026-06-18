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

    containerStats = docker_client.getContainerStats()

    for i in containerStats:
        net = i["networkI/O"]
        network_str = f"↑{net[0]:.2f} KB  ↓{net[1]:.2f} KB"

        table.add_row(
            i["name"],
            str(i["cpu_percent"]) + "%",
            str(i["memory_percent"]) + "%",
            network_str
        )    
    return table

def run():
    try:
        with Live(createTable(), refresh_per_second=2) as live:
            while True:
                time.sleep(0.5)
                live.update(createTable())
    except KeyboardInterrupt:
        print("\nClosing...")

if __name__ == "__main__":
    run()