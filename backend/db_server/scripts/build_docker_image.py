import os
import subprocess
from backend.db_server.docker_client.docker_utils import (
    get_docker_image_version,
    IMAGE_NAME,
    push_docker_image,
    update_docker_image_version,
)

DOCKER_USERNAME = os.environ["DOCKER_USERNAME"]
DOCKER_PASSWORD = os.environ["DOCKER_PASSWORD"]


def build_docker_image(
    docker_image_version_path="backend/db_server/docker_image_version/docker_image_version.py",
):
    os.chdir("..")

    current_version = get_docker_image_version(docker_image_version_path)

    # Increment the version number by 1
    version_parts = current_version.split(".")
    version_parts[-1] = str(int(version_parts[-1]) + 1)
    new_version = ".".join(version_parts)

    # Run the docker build command with the new tag and the path to the Dockerfile
    dockerfile_path = "Dockerfile"  # Path to the Dockerfile

    image = IMAGE_NAME.format(new_version)

    print("Building docker image")

    subprocess.run(
        [
            "docker",
            "build",
            "--platform",
            "linux/amd64",
            "-t",
            image,
            "-f",
            dockerfile_path,
            ".",
        ]
    )

    update_docker_image_version(new_version, docker_image_version_path)

    push_docker_image(DOCKER_USERNAME, DOCKER_PASSWORD, image)


build_docker_image()
