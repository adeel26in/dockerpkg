#!/usr/bin/env python3
import argparse
import docker
from docker.errors import DockerException, ImageNotFound, NotFound, APIError
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Docker client
try:
    client = docker.from_env()
except DockerException:
    print(Fore.RED + "Error: Could not connect to the Docker daemon. Is Docker running?")
    exit(1)

# -------------------
# IMAGE MANAGEMENT
# -------------------

def install_image(image_name):
    """Pull a Docker image with optional tag."""
    try:
        print(Fore.CYAN + f"Pulling image {image_name}...")
        client.images.pull(image_name)
        print(Fore.GREEN + f"Image {image_name} pulled successfully.")
    except ImageNotFound:
        print(Fore.RED + f"Error: Image '{image_name}' not found.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}")

def remove_image(image_name):
    try:
        client.images.remove(image=image_name, force=True)
        print(Fore.GREEN + f"Image {image_name} removed.")
    except ImageNotFound:
        print(Fore.RED + f"Error: Image '{image_name}' not found.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}")

def list_images():
    try:
        images = client.images.list()
        if not images:
            print(Fore.YELLOW + "No images found.")
            return
        print(f"{'ID':<15} IMAGE TAGS")
        for img in images:
            tags = img.tags if img.tags else ["<none>:<none>"]
            print(f"{Fore.WHITE}{img.short_id:<15} {Fore.CYAN}{tags}")
    except Exception as e:
        print(Fore.RED + f"Error listing images: {e}")

def update_image(image_name):
    try:
        print(Fore.CYAN + f"Updating image {image_name}...")
        client.images.pull(image_name)
        print(Fore.GREEN + f"Image {image_name} updated successfully.")
    except ImageNotFound:
        print(Fore.RED + f"Error: Image '{image_name}' not found.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}")

def update_all_images():
    try:
        images = client.images.list()
        if not images:
            print(Fore.YELLOW + "No images to update.")
            return
        for img in images:
            for tag in img.tags:
                print(Fore.CYAN + f"Updating {tag}...")
                client.images.pull(tag)
                print(Fore.GREEN + f"{tag} updated successfully.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}")

# -------------------
# CONTAINER MANAGEMENT
# -------------------

def run_container(image_name, name=None):
    try:
        kwargs = {"detach": True}
        if name:
            kwargs["name"] = name
        container = client.containers.run(image_name, **kwargs)
        print(Fore.GREEN + f"Container started: {container.name} (ID {container.id[:12]})")
    except ImageNotFound:
        print(Fore.RED + f"Error: Image '{image_name}' not found. Pull it first with 'dockerpkg install'.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}")

def start_container(identifier):
    try:
        container = client.containers.get(identifier)
        container.start()
        print(Fore.GREEN + f"Container '{container.name}' started.")
    except NotFound:
        print(Fore.RED + f"No container found with ID or name '{identifier}'.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")

def stop_container(identifier):
    try:
        container = client.containers.get(identifier)
        container.stop()
        print(Fore.GREEN + f"Container '{container.name}' stopped.")
    except NotFound:
        print(Fore.RED + f"No container found with ID or name '{identifier}'.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")

def restart_container(identifier):
    try:
        container = client.containers.get(identifier)
        container.restart()
        print(Fore.GREEN + f"Container '{container.name}' restarted.")
    except NotFound:
        print(Fore.RED + f"No container found with ID or name '{identifier}'.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")

def status_container(identifier):
    try:
        container = client.containers.get(identifier)
        status_color = Fore.GREEN if "running" in container.status else Fore.YELLOW
        print(f"Container '{container.name}' status: {status_color}{container.status}")
    except NotFound:
        print(Fore.RED + f"No container found with ID or name '{identifier}'.")

def remove_container(identifier):
    try:
        container = client.containers.get(identifier)
        container.remove(force=True)
        print(Fore.GREEN + f"Container '{identifier}' removed.")
    except NotFound:
        print(Fore.RED + f"No container found with ID or name '{identifier}'.")
    except APIError as e:
        print(Fore.RED + f"Docker API error: {e.explanation}")
    except Exception as e:
        print(Fore.RED + f"Unexpected error: {e}")

def list_containers():
    try:
        containers = client.containers.list(all=True)
        if not containers:
            print(Fore.YELLOW + "No containers found.")
            return
        print(f"{'ID':<15} {'NAME':<25} {'IMAGE':<25} STATUS")
        for c in containers:
            status_color = Fore.GREEN if "running" in c.status else Fore.YELLOW
            name = c.name
            image = c.image.tags[0] if c.image.tags else "<none>:<none>"
            print(f"{Fore.WHITE}{c.id[:12]:<15} {Fore.CYAN}{name:<25} {Fore.CYAN}{image:<25} {status_color}{c.status}")
    except Exception as e:
        print(Fore.RED + f"Error listing containers: {e}")

# -------------------
# MAIN CLI
# -------------------

def main():
    parser = argparse.ArgumentParser(description="dockerpkg - Docker package manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    # Image commands
    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("image", help="Image name with optional tag to install")

    removei_parser = subparsers.add_parser("removei")
    removei_parser.add_argument("image", help="Image name with optional tag to remove")

    subparsers.add_parser("listi")

    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("image", help="Image name with optional tag to update")

    subparsers.add_parser("update-all")

    # Container commands
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("image", help="Image name with optional tag to run a container from")
    run_parser.add_argument("--name", help="Optional container name")

    start_parser = subparsers.add_parser("start")
    start_parser.add_argument("container", help="Container ID or name to start")

    stop_parser = subparsers.add_parser("stop")
    stop_parser.add_argument("container", help="Container ID or name to stop")

    restart_parser = subparsers.add_parser("restart")
    restart_parser.add_argument("container", help="Container ID or name to restart")

    status_parser = subparsers.add_parser("status")
    status_parser.add_argument("container", help="Container ID or name to show status")

    removec_parser = subparsers.add_parser("removec")
    removec_parser.add_argument("container", help="Container ID or name to remove")

    subparsers.add_parser("listc")

    # Execute commands
    args = parser.parse_args()

    if args.command == "install":
        install_image(args.image)
    elif args.command == "removei":
        remove_image(args.image)
    elif args.command == "listi":
        list_images()
    elif args.command == "update":
        update_image(args.image)
    elif args.command == "update-all":
        update_all_images()
    elif args.command == "run":
        run_container(args.image, name=args.name)
    elif args.command == "start":
        start_container(args.container)
    elif args.command == "stop":
        stop_container(args.container)
    elif args.command == "restart":
        restart_container(args.container)
    elif args.command == "status":
        status_container(args.container)
    elif args.command == "removec":
        remove_container(args.container)
    elif args.command == "listc":
        list_containers()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
