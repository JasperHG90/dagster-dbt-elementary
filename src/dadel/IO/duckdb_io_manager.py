import os
import pathlib as plb
import typing

import duckdb
import pandas as pd
from dagster import (
    Field,
    InitResourceContext,
    InputContext,
    IOManager,
    OutputContext,
    StringSource,
    io_manager,
)

from .utils import connect_to_duckdb


class DuckdbParquetIOManager(IOManager):
    def __init__(
        self,
        path: str,
        aws_access_key: typing.Optional[str] = None,
        aws_secret_key: typing.Optional[str] = None,
        aws_endpoint: typing.Optional[str] = None,
        aws_region: typing.Optional[str] = None,
    ) -> None:
        if path.startswith(("s3://", "s3a://", "gs://")):
            self.path_is_local = False
        else:
            self.path_is_local = True
        self.path = path
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.aws_endpoint = aws_endpoint
        self.aws_region = aws_region

    def _get_table_name(self, asset_key: str, partition_key: typing.Optional[str] = None) -> str:
        if partition_key is not None:
            path = os.path.join(self.path, asset_key, f"{partition_key}.parquet")
            if self.path_is_local:
                _path = plb.Path(path)
                if not _path.parent.exists():
                    _path.parent.mkdir(parents=True, exist_ok=True)
        else:
            path = os.path.join(self.path, f"{asset_key}.parquet")
        return path

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        """Write a pandas DataFrame to disk using DuckDB"""
        path = self._get_table_name(
            partition_key=context.partition_key if context.has_partition_key else None,
            asset_key=context.asset_key.to_python_identifier(),
        )
        context.log.debug(obj.head())
        context.log.debug(path)
        context.log.debug(self.aws_endpoint)
        context.log.debug(f"Access key is None: {self.aws_access_key is None}")
        context.log.debug(f"Secret key is None: {self.aws_secret_key is None}")
        sql = f"COPY obj TO '{path}' (FORMAT 'parquet', row_group_size 100000);"
        context.log.debug(sql)
        con: duckdb.DuckDBPyConnection
        with connect_to_duckdb(
            ":memory:",
            self.aws_access_key,
            self.aws_secret_key,
            self.aws_region,
            self.aws_endpoint,
        ) as con:
            con.execute(sql)  # type: ignore
        context.add_output_metadata({"file_name": path})

    def load_input(self, context: InputContext) -> pd.DataFrame:
        """Load a pandas DataFrame using DuckDB"""
        context.log.debug(context.asset_partition_keys)
        if context.has_partition_key:
            path = [
                self._get_table_name(
                    partition_key=partition_key,
                    asset_key=context.upstream_output.asset_key.to_python_identifier(),
                )
                for partition_key in context.asset_partition_keys
            ]
        else:
            path = [
                self._get_table_name(
                    asset_key=context.upstream_output.asset_key.to_python_identifier(),
                )
            ]
        path = [f"'{p}'" for p in path]
        path_join = f'[{",".join(path)}]'
        sql = f"SELECT * FROM read_parquet({path_join})"
        context.log.debug(sql)
        con: duckdb.DuckDBPyConnection
        with connect_to_duckdb(
            ":memory:",
            self.aws_access_key,
            self.aws_secret_key,
            self.aws_region,
            self.aws_endpoint,
        ) as con:
            return con.sql(sql).df()  # type: ignore


@io_manager(
    config_schema={
        "path": StringSource,
        "aws_access_key": Field(StringSource, is_required=False),
        "aws_secret_key": Field(StringSource, is_required=False),
        "aws_endpoint": Field(StringSource, is_required=False),
        "aws_region": Field(StringSource, is_required=False),
    }
)
def duckdb_parquet_io_manager(
    init_context: InitResourceContext,
) -> DuckdbParquetIOManager:
    return DuckdbParquetIOManager(
        path=init_context.resource_config["path"],
        aws_access_key=init_context.resource_config.get("aws_access_key"),
        aws_secret_key=init_context.resource_config.get("aws_secret_key"),
        aws_endpoint=init_context.resource_config.get("aws_endpoint"),
        aws_region=init_context.resource_config.get("aws_region"),
    )
