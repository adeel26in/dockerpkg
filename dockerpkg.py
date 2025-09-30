#!/usr/bin/env python3
import argparse
import docker
from colorama import Fore, Style, init

init(autoreset=True)

# ------------------ Docker client helper ------------------
def get_client():
    """Return a Docker client connected to the environment."""
    try:
        return docker.from_env()
    except Exception as e:
        print(Fore.RED + f"Error: Could not connect to the Docker daemon. {e}")
        exit(1)

# ------------------ Image management ------------------
def install_image(image):
    client = get_client()
    try:
        print(Fore.CYAN + f"Pulling image {image}...")
        client.images.pull(image)
        print(Fore.GREEN + f"Image {image} installed successfully.")
    except Exception as e:
        print(Fore.RED + f"Failed to install image {image}: {e}")

def remove_image(image):
    client = get_client()
    try:
        client.images.remove(image, force=True)
        print(Fore.GREEN + f"Image {image} removed successfully.")
    except Exception as e:
        print(Fore.RED + f"Failed to remove image {image}: {e}")

def list_images():
    client = get_client()
    images = client.images.list()
    if not images:
        print(Fore.YELLOW + "No images found.")
        return
    print(Fore.CYAN + "Available images:")
    for img in images:
        tags = ", ".join(img.tags) if img.tags else "<none>"
        print(f"- {tags}")

# ------------------ Container management ------------------
def run_container(image):
    client = get_client()
    try:
        print(Fore.CYAN + f"Starting container from {image}...")
        container = client.containers.run(image, detach=True)
        print(Fore.GREEN + f"Container {container.short_id} running.")
    except Exception as e:
        print(Fore.RED + f"Failed to run container {image}: {e}")

def remove_container(container_id_or_name):
    client = get_client()
    try:
        container = client.containers.get(container_id_or_name)
        container.remove(force=True)
        print(Fore.GREEN + f"Container {container_id_or_name} removed successfully.")
    except Exception as e:
        print(Fore.RED + f"Failed to remove container {container_id_or_name}: {e}")

def list_containers():
    client = get_client()
    containers = client.containers.list(all=True)
    if not containers:
        print(Fore.YELLOW + "No containers found.")
        return
    print(Fore.CYAN + "Available containers:")
    for c in containers:
        print(f"- {c.name} ({c.short_id}) [{c.status}]")

# ------------------ Help ------------------
def show_help():
    print(Fore.MAGENTA + """
dockerpkg - APT-like package manager for Docker

Usage:
  dockerpkg install <image[:tag]>    Pull an image
  dockerpkg removei <image>          Remove an image
  dockerpkg run <image[:tag]>        Run a container (detached)
  dockerpkg removec <container>      Remove a container (by name or ID)
  dockerpkg listi                    List all images
  dockerpkg listc                    List all containers
  dockerpkg help                     Show this help message
""")

# ------------------ CLI parser ------------------
def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("target", nargs="?", help="Target (image or container)")
    args = parser.parse_args()

    if args.command == "install":
        install_image(args.target)
    elif args.command == "removei":
        remove_image(args.target)
    elif args.command == "run":
        run_container(args.target)
    elif args.command == "removec":
        remove_container(args.target)
    elif args.command == "listi":
        list_images()
    elif args.command == "listc":
        list_containers()
    elif args.command == "help" or args.command is None:
        show_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
