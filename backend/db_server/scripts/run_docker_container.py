import os
import subprocess

from backend.db_server.docker_client.docker_utils import (
    get_docker_image_version,
    get_start_container_cmd,
)

DOCKER_IMAGE_VERSION_PATH = "../docker_image_version/docker_image_version.py"
RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USERNAME = os.environ["RDS_USERNAME"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]


current_version = get_docker_image_version(DOCKER_IMAGE_VERSION_PATH)

start_container_cmd = get_start_container_cmd(
    RDS_ENDPOINT, RDS_USERNAME, RDS_PASSWORD, current_version
)

# Run the Docker command using subprocess
result = subprocess.run(start_container_cmd, shell=True, capture_output=True)

# Print the output
print(result.stderr.decode())

print(f"Running docker container: {current_version}")
