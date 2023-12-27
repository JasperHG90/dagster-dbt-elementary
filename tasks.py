import logging
import pathlib as plb
import shutil
from contextlib import contextmanager

import sh
from invoke import task

logger = logging.getLogger("tasks")
handler = logging.StreamHandler()
format = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
handler.setFormatter(format)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

fp = plb.Path(__file__).parent.absolute()
dagster_home = fp / ".dagster"
dagster_conf = fp / "dagster.yaml"
tmp = fp / ".tmp"
postgres_data = tmp / "postgres_data"


@contextmanager
def _stop_postgres_on_exit():
    postgres_data.mkdir(exist_ok=True)
    logger.info("Starting postgres container")
    uid = sh.docker.run(
        "-e",
        "POSTGRES_USER=dbt",
        "-e",
        "POSTGRES_PASSWORD=dbt",
        "-e",
        "POSTGRES_DB=dbt",
        "-p",
        "5432:5432",
        "-h",
        "0.0.0.0",
        "-d",
        "-v",
        f"{str(postgres_data)}:/var/lib/postgresql/data",
        "--rm",
        "postgres:16.1",
    ).strip()
    try:
        yield
    except sh.ErrorReturnCode:
        logger.error("Error running docker container")
        sh.docker.stop(uid)
    finally:
        logger.info("Stopping postgres container")
        sh.docker.stop(uid)


@task()
def dagster_dev(c):
    """Run the dagster development environment"""
    logger.info(f"Setting dagster home to '{dagster_home}'")
    dagster_home.mkdir(exist_ok=True)
    logger.info(f"Setting temporary data directory to '{tmp}'")
    tmp.mkdir(exist_ok=True)
    logger.info(f"Copying dagster config to '{dagster_home}'")
    shutil.copy(
        dagster_conf,
        dagster_home / "dagster.yaml",
    )
    with _stop_postgres_on_exit():
        logger.info("Running local dagster development environment")
        c.run(f'DAGSTER_HOME="{dagster_home}" poetry run dagster dev')
