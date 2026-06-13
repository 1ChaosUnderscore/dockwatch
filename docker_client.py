import docker
import json

try:  
    client = docker.from_env()
except Exception as e:
    print("Unable To Find Contaner")
    exit(1)

containers = client.containers.list()

def calculate_cpu_percent(data):
    cpu_delta = data["cpu_stats"]["cpu_usage"]["total_usage"] - \
                data["precpu_stats"]["cpu_usage"]["total_usage"]

    system_delta = data["cpu_stats"]["system_cpu_usage"] - \
                    data["precpu_stats"]["system_cpu_usage"]

    num_cpus = data["cpu_stats"].get("online_cpus", 1)

    if system_delta > 0 and cpu_delta > 0:
        return (cpu_delta / system_delta) * num_cpus * 100.0
    return 0.0

for i in containers:
    stats = i.stats(stream=True, decode=True)
    data = next(stats)

    calculate_cpu_percent(data)

    print(json.dumps(data["cpu_stats"], indent=2))