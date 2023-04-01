import logging
import os
import subprocess
import re

logger = logging.getLogger(__name__)

DOCKER_USERNAME = os.environ["DOCKER_USERNAME"]
DOCKER_PASSWORD = os.environ["DOCKER_PASSWORD"]


os.chdir("..")


docker_image_version_path = (
    "backend/db_server/docker_image_version/docker_image_version.py"
)

# Read the current version from version.py
with open(docker_image_version_path, "r") as f:
    version_file = f.read()
current_version = re.search(
    r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', version_file, re.MULTILINE
).group(1)

# Increment the version number by 1
version_parts = current_version.split(".")
version_parts[-1] = str(int(version_parts[-1]) + 1)
new_version = ".".join(version_parts)

# Run the docker build command with the new tag and the path to the Dockerfile
dockerfile_path = "Dockerfile"  # Path to the Dockerfile
tag = f"barsela/wifix_db_server:{new_version}"

logger.info("Building docker image")

subprocess.run(["docker", "build", "--platform", "linux/amd64", "-t", tag, "-f", dockerfile_path, "."])

# Update the version.py file with the new version number
with open(docker_image_version_path, "w") as f:
    f.write(f'__version__ = "{new_version}"\n')


# Login to Docker Hub
logger.info("Logining to docker hub")
subprocess.run(["docker", "login", "-u", DOCKER_USERNAME, "-p", DOCKER_PASSWORD])

# Push the Docker image to Docker Hub
logger.info("Pushing to docker hub")
subprocess.run(["docker", "push", tag])
