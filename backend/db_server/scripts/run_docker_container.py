import os
import re
import subprocess

RDS_ENDPOINT = os.environ["RDS_ENDPOINT"]
RDS_USERNAME = os.environ["RDS_USERNAME"]
RDS_PASSWORD = os.environ["RDS_PASSWORD"]

container_name = "wifix_db_server_container"
image_name = "barsela/wifix_db_server"
docker_image_version_path = "../docker_image_version/docker_image_version.py"

# Read the current version from version.py
with open(docker_image_version_path, "r") as f:
    version_file = f.read()
current_version = re.search(
    r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', version_file, re.MULTILINE
).group(1)

# Build the Docker command
docker_cmd = (
    f"docker run -p 8080:8080 "
    f"--name {container_name}_{current_version} "
    f"-e RDS_ENDPOINT={RDS_ENDPOINT} "
    f"-e RDS_PASSWORD={RDS_PASSWORD} "
    f"-e RDS_USERNAME={RDS_USERNAME} "
    f"{image_name}:{current_version}"
)

# Run the Docker command using subprocess
result = subprocess.run(docker_cmd, shell=True, capture_output=True)

# Print the output
print(result.stderr.decode())
