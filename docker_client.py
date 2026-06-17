import docker
import math
import json

try:  
    client = docker.from_env()
except Exception as e:
    print("Unable to find container, do you have containers running?")
    exit(1)

containers = client.containers.list()
containerStats = []

#calculates the percentage of the given data's cpu percent
def calculateCPUpercent(data):
    cpuStats = data["cpu_stats"]

    total_cpu = cpuStats["cpu_usage"]["total_usage"]
    currentSystem = cpuStats["system_cpu_usage"]
    online_cpus = cpuStats["online_cpus"]

    preTotal_cpu = data["precpu_stats"]["cpu_usage"]["total_usage"]
    previousSystem = data["precpu_stats"].get("system_cpu_usage", 0)

    cpuDelta = total_cpu - preTotal_cpu
    systemDelta = currentSystem - previousSystem

    cpuPercent = (cpuDelta / systemDelta) * online_cpus * 100

    if systemDelta > 0 and cpuDelta > 0:
        return math.ceil(cpuPercent * 1000) / 1000
    return 0

#calculates the percentage of the given data's memory percent
def calculateMemoryPercent(data):
    memoryStats = data["memory_stats"]

    memoryUsage = memoryStats["usage"]
    memoryLimit = memoryStats["limit"]
    memoryCache = memoryStats["stats"].get("inactive_file") or memoryStats["stats"].get("cache", 0)

    memoryUsed = memoryUsage - memoryCache

    memoryPercent = (memoryUsed / memoryLimit) * 100
    if memoryUsage > 0 and memoryLimit > 0:
        return math.ceil(memoryPercent * 1000) / 1000
    return 0

#calculates the upload and download speed of the given data
def calculateNetwork(data):

    if "networks" not in data:
        return 0, 0

    networkStats = data["networks"]

    totalRX = 0
    totalTX = 0

    for i, network_stats in networkStats.items():
        rx = network_stats["rx_bytes"]
        tx = network_stats["tx_bytes"]

        totalRX += rx
        totalTX += tx
    
    KBtx = totalTX / 1024
    KBrx = totalRX / 1024

    return KBtx, KBrx

def getContainerStats():
    return containerStats

#loops through each container
for i in containers:
    stats = i.stats(stream=True, decode=True)

    next(stats)
    data = next(stats)

    containerStats.append({
        "name": i.name,
        "cpu_percent": calculateCPUpercent(data),
        "memory_percent": calculateMemoryPercent(data),
        "networkI/O": calculateNetwork(data)
    })

    #print(json.dumps(data, indent=2))