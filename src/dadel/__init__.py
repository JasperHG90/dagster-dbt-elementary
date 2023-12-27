from importlib import metadata

from dadel.assets import (
    air_quality_data,
    archive_ingested_data,
    copy_to_data_lake,
    normalize_data,
    split_formulas,
)
from dadel.assets.checks import values_between_01
from dadel.jobs import ingestion_job
from dadel.sensors import stations_sensor
from dagster import Definitions
from dadel.IO.io_manager import duckdb_parquet_io_manager
from dadel.IO.resources import LuchtMeetNetResource

try:
    __version__ = metadata.version("dadel")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"


shared_resources = {"luchtmeetnet_api": LuchtMeetNetResource()}

env_resources = {
    "dev": shared_resources
    | {
        "landing_zone": duckdb_parquet_io_manager.configured(
            {"path": ".tmp/landing_zone"}
        )
    }
    | {
        "archive": duckdb_parquet_io_manager.configured(
            {"path": ".tmp/archive"}
        )
    }
}

definition = Definitions(
    assets=[
        air_quality_data,
        copy_to_data_lake,
        normalize_data,
        split_formulas,
        archive_ingested_data,
    ],
    resources=env_resources["dev"],
    jobs=[ingestion_job],
    asset_checks=[values_between_01],
    sensors=[stations_sensor],
)
