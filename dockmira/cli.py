import click
import display

@click.group()
def cli():
    """\b
    ██████╗  ██████╗  ██████╗██╗  ██╗███╗   ███╗██╗██████╗  █████╗ 
    ██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝████╗ ████║██║██╔══██╗██╔══██╗
    ██║  ██║██║   ██║██║     █████╔╝ ██╔████╔██║██║██████╔╝███████║
    ██║  ██║██║   ██║██║     ██╔═██╗ ██║╚██╔╝██║██║██╔══██╗██╔══██║
    ██████╔╝╚██████╔╝╚██████╗██║  ██╗██║ ╚═╝ ██║██║██║  ██║██║  ██║
    ╚═════╝  ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
    ───────────────────────────────────────────────────────────────
                                                               
    A real-time Docker container health monitoring from your terminal
    """
    pass

@cli.command()
def watch():
    """Watch all running containers"""
    display.main()

@cli.command()
def list():
    """List all running containers and their current stats once."""
    from dockmira import docker_client
    stats = docker_client.getContainerStats()
    for s in stats:
        print(f"{s['name']}: CPU {s['cpu_percent']}% | RAM {s['memory_percent']}%")

if __name__ == "__main__":
    cli()