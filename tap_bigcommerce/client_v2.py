from typing import Any, Dict, Optional

import requests

from tap_bigcommerce.client_base import BigcommerceStream


class BigcommerceV2Stream(BigcommerceStream):
    """hubspot stream class."""

    records_jsonpath = "$[*]"
    consignments = []
    order_items = []

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
        if next_page_token:
            params["page"] = next_page_token
        if self.replication_key:
            start_date = self.get_starting_time(context)
            if start_date:
                params["min_date_modified"] = start_date.isoformat()
        if hasattr(self, "additional_params"):
            params.update(self.additional_params)
        return params
