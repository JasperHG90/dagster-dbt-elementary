from typing import Any, Dict, List, Optional

from dagster import ConfigurableResource
from delt.api import get_results_luchtmeetnet_endpoint


class LuchtMeetNetResource(ConfigurableResource):
    def request(
        self, endpoint: str, request_params: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        context = self.get_resource_context()
        context.log.debug(endpoint)
        context.log.debug(request_params)
        return get_results_luchtmeetnet_endpoint(endpoint=endpoint, request_params=request_params)
