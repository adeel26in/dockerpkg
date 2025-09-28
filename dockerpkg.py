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

def install_image(image_name):
    try:
        print(Fore.CYAN + f"Pulling image {image_name}...")
        client.images.pull(image_name)
        print(Fore.GREEN + f"Image {image_name} pulled successfully.")
        
        print(Fore.CYAN + f"Running container from {image_name} in detached mode...")
        container = client.containers.run(image_name, detach=True)
        print(Fore.GREEN + f"Container started with ID {container.id[:12]}.")
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

def remove_container(identifier):
    try:
        container = client.containers.get(identifier)  # works with ID or name
        container.remove(force=True)
        print(Fore.GREEN + f"Container '{identifier}' removed.")
    except NotFound:
        print(Fore.RED + f"Error: No container found with ID or name '{identifier}'.")
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

def main():
    parser = argparse.ArgumentParser(description="dockerpkg - Simple Docker package manager")
    subparsers = parser.add_subparsers(dest="command")

    # install
    install_parser = subparsers.add_parser("install")
    install_parser.add_argument("image", help="Image name to install and run")

    # remove image
    removei_parser = subparsers.add_parser("removei")
    removei_parser.add_argument("image", help="Image name to remove")

    # remove container
    removec_parser = subparsers.add_parser("removec")
    removec_parser.add_argument("container", help="Container ID or name to remove")

    # list containers
    subparsers.add_parser("listc")

    # list images
    subparsers.add_parser("listi")

    args = parser.parse_args()

    if args.command == "install":
        install_image(args.image)
    elif args.command == "removei":
        remove_image(args.image)
    elif args.command == "removec":
        remove_container(args.container)
    elif args.command == "listc":
        list_containers()
    elif args.command == "listi":
        list_images()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
