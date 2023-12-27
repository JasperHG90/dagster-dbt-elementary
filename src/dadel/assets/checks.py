from dagster import AssetCheckResult, asset_check
import pandas as pd

from dag_advanced.assets import normalize_data


@asset_check(
    asset=normalize_data,
)
def values_between_01(normalize_data: pd.DataFrame):
    check = normalize_data.min()["value_norm"] >= 0 and normalize_data.max()["value_norm"] <= 1
    return AssetCheckResult(
        passed=bool(check)
    )
