# You would need to install the docker provider package:
# pip install apache-airflow-providers-docker

from airflow.providers.docker.operators.docker import DockerOperator

# ... inside your DAG file ...

run_container_with_docker_operator = DockerOperator(
    task_id="run_py_file_proc_with_docker_operator",
    image="py-file-proc",
    auto_remove=True,
    command="python main.py",
    environment={
        "APP_ENV": TARGET_ENVIRONMENT
    },
    docker_url="unix://var/run/docker.sock",  # Or your Docker daemon TCP URL
    network_mode="bridge" # Or the network mode your container needs
)