from typing import Any, Dict, Optional

import requests

from tap_bigcommerce.client_base import BigcommerceStream


class BigcommerceV2Stream(BigcommerceStream):
    """hubspot stream class."""

    records_jsonpath = "$[*]"

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        status_code = response.status_code
        previous_token = previous_token or 1

        if status_code == 204:
            next_page_token = None
        else:
            next_page_token = previous_token + 1
        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if self.filter_by_channel_id_in_query_string and self.config.get("channel_id"):
            params["channel_id"] = self.config.get("channel_id")
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            start_date = self.get_starting_time(context, is_inclusive=True)
            if start_date:
                params["min_date_modified"] = start_date.isoformat()
        return params
