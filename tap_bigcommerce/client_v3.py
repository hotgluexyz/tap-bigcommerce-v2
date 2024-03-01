from typing import Any, Dict, Optional

import requests

from tap_bigcommerce.client_base import BigcommerceStream


class BigcommerceV3Stream(BigcommerceStream):
    """hubspot stream class."""

    def get_next_page_token(
        self, response: requests.Response, previous_token: Optional[Any]
    ) -> Optional[Any]:
        """Return a token for identifying next page or None if no more pages."""
        if response.status_code == 204:
            return None
        response_json = response.json()
        next_page_token = None

        if "meta" in response_json:
            if not response_json["meta"]:
                return None
            current_page = response_json["meta"]["pagination"]["current_page"]
            total_pages = response_json["meta"]["pagination"]["total_pages"]
            if current_page < total_pages:
                next_page_token = current_page + 1
        else:
            next_page_token = None
        return next_page_token

    def get_url_params(
        self, context: Optional[dict], next_page_token: Optional[Any]
    ) -> Dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            start_date = self.get_starting_time(context)
            if start_date:
                params["date_modified:min"] = start_date.strftime('%Y-%m-%dT%H:%M:%S+00:00')
        return params
