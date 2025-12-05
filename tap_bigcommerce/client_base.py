"""REST client handling, including BigcommerceStream base class."""

from typing import Callable, Iterable, Optional

import backoff
import requests
import datetime
from pendulum import parse
from singer_sdk.streams import RESTStream
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath

import singer
from singer import StateMessage

class BigcommerceStream(RESTStream):
    """Bigcommerce stream class."""
    extra_retry_statuses = [429,422,401]
    filter_by_channel_id_in_query_string = False
    filter_by_channel_id_in_body = False

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        hash = self.config.get("store_hash")
        return f"https://api.bigcommerce.com/stores/{hash}"

    records_jsonpath = "$[*]"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        """Return a new authenticator object."""
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="X-Auth-Token",
            value=str(self.config.get("access_token")),
            location="header",
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        headers = {}
        headers["Accept"] = "application/json"
        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")
        return headers

    def get_starting_time(self, context):
        start_date = self.config.get("start_date")
        if start_date:
            start_date = parse(self.config.get("start_date"))
        rep_key = self.get_starting_timestamp(context) + datetime.timedelta(seconds=1)
        return rep_key or start_date

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        if response.status_code != 204:
            yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    @staticmethod
    def _url_encode(val) -> str:
        return str(val)

    def request_decorator(self, func):
        decorator = backoff.on_exception(
            self.backoff_wait_generator,
            (
                RetriableAPIError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
            ),
            max_tries=self.backoff_max_tries,
            on_backoff=self.backoff_handler,
        )(func)
        return decorator


    def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
        channel_id = self.config.get("channel_id")
        # if filter_by_channel_id_in_body is True and channel_id is provided,
        # filter the record by the channel_id
        if self.filter_by_channel_id_in_body and channel_id:
            # looks for the given record fields:
            # `channel_id` is an integer
            # `channel_ids` is an array of integers
            # `origin_channel_id` is an integer
            record_channel_ids = row.get("channel_ids") or []
            if row.get("channel_id") == channel_id \
                or row.get("origin_channel_id") == channel_id \
                or channel_id in record_channel_ids:
                return row
            return None
        return row


    def _write_state_message(self) -> None:
        """Write out a STATE message with the latest state."""
        tap_state = self.tap_state

        if tap_state and tap_state.get("bookmarks"):
            for stream_name in tap_state.get("bookmarks").keys():
                if tap_state["bookmarks"][stream_name].get("partitions"):
                    tap_state["bookmarks"][stream_name] = {"partitions": []}

        singer.write_message(StateMessage(value=tap_state))