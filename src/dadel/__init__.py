from importlib import metadata

from dagster import Definitions

from dadel.assets import air_quality_data
from dadel.IO.duckdb_io_manager import duckdb_parquet_io_manager
from dadel.IO.resources import LuchtMeetNetResource
from dadel.jobs import ingestion_job
from dadel.sensors import stations_sensor

try:
    __version__ = metadata.version("dadel")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"


shared_resources = {"luchtmeetnet_api": LuchtMeetNetResource()}

env_resources = {
    "dev": shared_resources
    | {"landing_zone": duckdb_parquet_io_manager.configured({"path": ".tmp/landing_zone"})}
}

definition = Definitions(
    assets=[
        air_quality_data,
    ],
    resources=env_resources["dev"],
    jobs=[ingestion_job],
    sensors=[stations_sensor],
)
