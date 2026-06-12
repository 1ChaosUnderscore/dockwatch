import docker

def main():
    try :
        client = docker.from_env()
    except:
        print("Unable To Retrieve Client.")
        return

    containers = client.containers.list()

    for i in containers:
        print(i.name, i.id[:12])

if __name__ == "__main__":
    main()