import os
from typing import Tuple

import pandas as pd
from dagster import AssetOut, AssetIn, asset, multi_asset, AutoMaterializePolicy, FreshnessPolicy
from dadel.IO.resources import LuchtMeetNetResource
from dadel.transformations import groupby_min_max_normalize
from dadel.utils import split_df_column

from dadel.partitions import daily_station_partition, daily_partition


@asset(
    description="Air quality data from the Luchtmeetnet API",
    compute_kind="duckdb",
    io_manager_key="duckdb_io_landing_zone",
    partitions_def=daily_station_partition,
    auto_materialize_policy=AutoMaterializePolicy.eager(
        max_materializations_per_minute=None
    )
)
def air_quality_data(context, luchtmeetnet_api: LuchtMeetNetResource) -> pd.DataFrame:
    date, station = context.partition_key.split("|")
    context.log.debug(date)
    context.log.debug(f"Fetching data for {date}")
    rp = {"start": f"{date}T00:00:00", "end": f"{date}T23:59:59", "station_number": station}
    df = pd.DataFrame(luchtmeetnet_api.request("measurements", request_params=rp))
    context.log.debug(df.head())
    return df


# @asset(
#     description="Copy data from landing zone to postgresql",
#     compute_kind="duckdb",
#     io_manager_key="duckdb_io_data_lake",
#     partitions_def=daily_partition,
#     ins={"ingested_data": AssetIn(
#             "air_quality_data",
#             input_manager_key="duckdb_io_landing_zone",
#         )
#     },
#     auto_materialize_policy=AutoMaterializePolicy.eager(
#         # See: https://docs.dagster.io/concepts/assets/asset-auto-execution#auto-materialization-and-partitions
#         max_materializations_per_minute=None
#     )
# )
# def copy_to_data_lake(context, ingested_data: pd.DataFrame) -> pd.DataFrame:
#     return ingested_data


# @asset(
#     description="Archive ingested data",
#     compute_kind="python",
#     ins={"ingested_data": AssetIn(
#             "air_quality_data",
#             input_manager_key="duckdb_io_landing_zone",
#         )
#     },
#     non_argument_deps={"copy_to_data_lake"},
#     io_manager_key="duckdb_io_archive",
#     partitions_def=daily_partition,
#     auto_materialize_policy=AutoMaterializePolicy.eager(
#         # See: https://docs.dagster.io/concepts/assets/asset-auto-execution#auto-materialization-and-partitions
#         max_materializations_per_minute=None
#     )
# )
# def archive_ingested_data(context, ingested_data: pd.DataFrame):
#     upstream_path = context.resources.duckdb_io_landing_zone.path
#     upstream_asset_key = context.asset_key_for_input("ingested_data").to_python_identifier()
#     context.log.debug(context.asset_partition_keys_for_input("ingested_data"))
#     upstream_partition_key = context.asset_partition_key_for_input("ingested_data")

#     # If path is local ...
#     path = os.path.join(upstream_path, upstream_asset_key, f"{upstream_partition_key}.parquet")
#     os.remove(path)
#     # Else ...
#     return ingested_data
