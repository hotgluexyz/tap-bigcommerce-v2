"""REST client handling, including BigcommerceStream base class."""

from typing import Callable, Iterable

import backoff
import requests
import datetime
from pendulum import parse
from singer_sdk.streams import RESTStream
from singer_sdk.exceptions import FatalAPIError, RetriableAPIError
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath


class BigcommerceStream(RESTStream):
    """Bigcommerce stream class."""

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
