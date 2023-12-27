from dadel.jobs import ingestion_job
from dadel.partitions import stations_partition
from dagster import SensorResult, sensor
from dadel.IO.resources import LuchtMeetNetResource


@sensor(job=ingestion_job)
def stations_sensor(context, luchtmeetnet_api: LuchtMeetNetResource):
    # Only take first three stations for demo purposes
    stations_request = luchtmeetnet_api.request("stations")[:2]
    context.log.debug(stations_request)
    stations = [
        f["number"]
        for f in stations_request
        if not context.instance.has_dynamic_partition(stations_partition.name, f["number"])
    ]
    context.log.debug(stations)
    return SensorResult(
        run_requests=None,
        dynamic_partitions_requests=[stations_partition.build_add_request(stations)],
    )
