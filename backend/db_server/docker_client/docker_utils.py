import re
import subprocess

from backend.db_server.logger_client import logger

CONTAINER_NAME = "wifix_db_server_container_{}"
IMAGE_NAME = "barsela/wifix_db_server:{}"


def get_docker_image_version(docker_image_version_path: str) -> str:
    with open(docker_image_version_path, "r") as f:
        version_file = f.read()
    current_version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', version_file, re.MULTILINE
    ).group(1)

    return current_version


def push_docker_image(docker_username: str, docker_password: str, image: str):
    # Login to Docker Hub
    logger.info("Logining to docker hub")
    subprocess.run(["docker", "login", "-u", docker_username, "-p", docker_password])

    # Push the Docker image to Docker Hub
    logger.info("Pushing to docker hub")
    subprocess.run(["docker", "push", image])
    logger.info(f"Pushed image: {image}")


def get_start_container_cmd(
    rds_endpoint: str, rds_username: str, rds_password: str, current_version: str
) -> str:
    start_container_cmd = (
        f"docker run -d -p 8080:8080 "
        f"--name {CONTAINER_NAME.format(current_version)} "
        f"-e RDS_ENDPOINT={rds_endpoint} "
        f"-e RDS_PASSWORD={rds_password} "
        f"-e RDS_USERNAME={rds_username} "
        f"{IMAGE_NAME.format(current_version)}"
    )
    return start_container_cmd


def update_docker_image_version(new_version: str, docker_image_version_path: str):
    with open(docker_image_version_path, "w") as f:
        f.write(f'__version__ = "{new_version}"\n')
