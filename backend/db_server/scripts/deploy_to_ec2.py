import os
from typing import List, Dict

import paramiko

from backend.db_server.docker_client.docker_utils import (
    get_start_container_cmd,
    get_docker_image_version,
)
from backend.db_server.logger_client import logger

RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USERNAME = os.environ["RDS_USERNAME"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]
PRIVATE_KEY_FILE = os.environ["PRIVATE_KEY_FILE"]
EC2_HOSTNAME = os.environ["EC2_HOSTNAME"]
EC2_USERNAME = "ec2-user"
DOCKER_IMAGE_VERSION_PATH = "../docker_image_version/docker_image_version.py"


class SSHClient:
    def __init__(self):
        logger.info("Connecting to SSH")
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(
            EC2_HOSTNAME, username=EC2_USERNAME, key_filename=PRIVATE_KEY_FILE
        )

    def __del__(self):
        self.ssh.close()

    def _execute_commands(self, commands: List[str]) -> List[str]:
        info = []
        for command in commands:
            logger.info(f"Executing command: {command}")
            stdin, stdout, stderr = self.ssh.exec_command(command)
            info.append(stdout.read().decode())

        return info

    def _get_exist_docker_containers(self) -> Dict[str, Dict[str, str]]:
        containers_dict: Dict[str, Dict[str, str]] = {}
        logger.info(f"Getting docker containers list")

        ps_command = "sudo docker container ls -a"
        containers_info = self._execute_commands([ps_command])[0]

        containers = containers_info.split("\n")
        containers = containers[1:]

        for container in containers:
            if container:
                container_info = container.split()
                container_id: str = container_info[0]
                container_name: str = container[8]
                image_name: str = container[1]
                containers_dict[container_id] = {
                    "container_id": container_id,
                    "container_name": container_name,
                    "image_name": image_name,
                }

        return containers_dict

    def _terminate_docker_containers(self):

        containers: Dict[str, Dict[str, str]] = self._get_exist_docker_containers()

        for container in containers.values():
            logger.info("Terminate Docker Container:")
            logger.info(f"Container ID: {container['container_id']}")
            logger.info(f"Container Name: {container['container_name']}")
            logger.info(f"Image Name: {container['image_name']}")

            logger.info("Terminating docker containers")

            terminate_commands = [
                f"sudo docker stop {container['container_id']}",
                f"sudo docker rm {container['container_id']}",
            ]
            response = self._execute_commands(terminate_commands)

            if (
                container["container_id"] not in response[0]
                or container["container_id"] not in response[1]
            ):
                raise Exception(
                    f"Failed to terminate container_id: {container['container_id']}"
                )

            logger.info(f"Docker containers terminated")

    def _get_docker_images(self):
        images_dict: Dict[str, Dict[str, str]] = {}
        logger.info(f"Getting docker images list")

        ps_command = "sudo docker image ls -a"
        images_info = self._execute_commands([ps_command])[0]

        images = images_info.split("\n")
        images = images[1:]

        for image in images:
            if image:
                image_info = image.split()
                image_id: str = image_info[2]
                image_name_and_tag: str = f"{image_info[0]}:{image_info[1]}"
                images_dict[image_id] = {
                    "image_id": image_id,
                    "image_name_and_tag": image_name_and_tag,
                }

        return images_dict

    def _remove_docker_images(self):
        images_dict: Dict[str, Dict[str, str]] = self._get_docker_images()

        for image in images_dict.values():
            logger.info("Removing Docker Image:")
            logger.info(f"Image Name: {image['image_name_and_tag']}")
            logger.info(f"Image ID: {image['image_id']}")

            terminate_commands = [f"sudo docker image rm {image['image_id']}"]

            self._execute_commands(terminate_commands)

            logger.info(f"Docker images removed")

    def _pull_last_docker_image(self):
        version = get_docker_image_version(DOCKER_IMAGE_VERSION_PATH)
        image: str = f"barsela/wifix_db_server:{version}"

        logger.info(f"Pulling docker image: {image}")

        pull_docker_image_command = f"sudo docker pull {image}"
        self._execute_commands([pull_docker_image_command])

        logger.info(f"Docker image pulled")

    def _start_docker_container(self):
        current_version = get_docker_image_version(DOCKER_IMAGE_VERSION_PATH)
        logger.info(f"Starting docker container, version: {current_version}")

        start_container_cmd = f"sudo {get_start_container_cmd(RDS_ENDPOINT, RDS_USERNAME, RDS_PASSWORD, current_version)}"
        self._execute_commands([start_container_cmd])

        logger.info("Docker container started")

    def deploy_to_ec2(self, build_image: bool = False):
        if build_image:
            from backend.db_server.scripts.build_docker_image import build_docker_image

            docker_image_version_path = "docker_image_version/docker_image_version.py"
            build_docker_image(docker_image_version_path)

        self._terminate_docker_containers()
        self._remove_docker_images()
        self._pull_last_docker_image()
        self._start_docker_container()


ssh_client = SSHClient()
ssh_client.deploy_to_ec2(build_image=False)
