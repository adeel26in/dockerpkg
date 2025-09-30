#!/usr/bin/env python3
import docker
import argparse
import os
import sys


def get_client():
    """Return a Docker client that behaves like the docker CLI."""
    docker_host = os.environ.get("DOCKER_HOST")
    try:
        if docker_host:
            return docker.DockerClient(base_url=docker_host)
        return docker.DockerClient(base_url="unix:///var/run/docker.sock")
    except PermissionError:
        print("❌ Permission denied while connecting to Docker.")
        print("👉 Fix: Add your user to the docker group and re-login:")
        print("   sudo usermod -aG docker $USER")
        print("   newgrp docker   # or log out and back in")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Could not connect to the Docker daemon. {e}")
        sys.exit(1)


def install_image(image_name):
    client = get_client()
    print(f"Pulling image: {image_name}")
    try:
        client.images.pull(image_name)
        print(f"✅ Image '{image_name}' installed successfully.")
    except Exception as e:
        print(f"Error: {e}")


def remove_image(image_name):
    client = get_client()
    print(f"Removing image: {image_name}")
    try:
        client.images.remove(image=image_name, force=True)
        print(f"✅ Image '{image_name}' removed successfully.")
    except Exception as e:
        print(f"Error: {e}")


def remove_container(container_name):
    client = get_client()
    print(f"Removing container: {container_name}")
    try:
        container = None
        try:
            container = client.containers.get(container_name)
        except docker.errors.NotFound:
            containers = client.containers.list(all=True, filters={"name": container_name})
            if containers:
                container = containers[0]
        if container:
            container.remove(force=True)
            print(f"✅ Container '{container_name}' removed successfully.")
        else:
            print(f"Error: Container '{container_name}' not found.")
    except Exception as e:
        print(f"Error: {e}")


def list_containers():
    client = get_client()
    try:
        containers = client.containers.list(all=True)
        if not containers:
            print("No containers found.")
        else:
            print("Containers:")
            for container in containers:
                print(f" - {container.name} ({container.id[:12]}) - {container.status}")
    except Exception as e:
        print(f"Error: {e}")


def list_images():
    client = get_client()
    try:
        images = client.images.list()
        if not images:
            print("No images found.")
        else:
            print("Images:")
            for image in images:
                tags = ", ".join(image.tags) if image.tags else "<none>"
                print(f" - {image.short_id} {tags}")
    except Exception as e:
        print(f"Error: {e}")


def doctor():
    """Run diagnostic checks for Docker connectivity."""
    print("🔎 Running dockerpkg doctor...")
    try:
        client = get_client()
        version = client.version()
        print(f"✅ Connected to Docker daemon (API version: {version['ApiVersion']})")

        client.images.list()
        print("✅ Able to list images")

        client.containers.list(all=True)
        print("✅ Able to list containers")

        print("🎉 All checks passed!")
    except PermissionError:
        print("❌ Permission denied. Try adding your user to the docker group:")
        print("   sudo usermod -aG docker $USER")
        print("   newgrp docker")
    except Exception as e:
        print(f"❌ Doctor check failed: {e}")


def main():
    parser = argparse.ArgumentParser(
        prog="dockerpkg",
        description="dockerpkg: A package manager–like CLI for Docker"
    )

    subparsers = parser.add_subparsers(dest="command")

    # install
    install_parser = subparsers.add_parser("install", help="Install (pull) an image")
    install_parser.add_argument("image", help="Image name (e.g., nginx:latest)")

    # removei
    removei_parser = subparsers.add_parser("removei", help="Remove an image")
    removei_parser.add_argument("image", help="Image name (e.g., nginx:latest)")

    # removec
    removec_parser = subparsers.add_parser("removec", help="Remove a container")
    removec_parser.add_argument("container", help="Container name or ID")

    # listc
    subparsers.add_parser("listc", help="List all containers")

    # listi
    subparsers.add_parser("listi", help="List all images")

    # doctor
    subparsers.add_parser("doctor", help="Run diagnostic checks")

    # help
    subparsers.add_parser("help", help="Show help message")

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
    elif args.command == "doctor":
        doctor()
    elif args.command == "help" or args.command is None:
        parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
