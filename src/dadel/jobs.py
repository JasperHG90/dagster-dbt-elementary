from dag_advanced.assets import air_quality_data
from dag_advanced.partitions import daily_station_partition
from dagster import define_asset_job

ingestion_job = define_asset_job(
    name="ingestion_job",
    selection=[air_quality_data],
    description="Ingestion job for air quality data",
    partitions_def=daily_station_partition,
    config={
        "execution": {
            "config": {
                "multiprocess": {
                    "max_concurrent": 4,
                },
            }
        }
    },
)
