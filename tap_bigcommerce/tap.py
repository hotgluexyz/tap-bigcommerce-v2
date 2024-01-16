"""Bigcommerce tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th

from tap_bigcommerce.streams import (
    CategoriesStream,
    CouponsStream,
    CustomersStream,
    OrdersStream,
    ProductsStream,
    VariantsStream,
    OrderLinesStream,
    RefundsStream,
    OrderShippingAddressStream,
    OrderConsignmentsStream
)

STREAM_TYPES = [
    CategoriesStream,
    CustomersStream,
    ProductsStream,
    CouponsStream,
    OrdersStream,
    VariantsStream,
    OrderLinesStream,
    RefundsStream,
    OrderShippingAddressStream,
    OrderConsignmentsStream
]


class TapBigcommerce(Tap):
    """Bigcommerce tap class."""

    name = "tap-bigcommerce"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "store_hash",
            th.StringType,
            required=True,
            description="Store Hash",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapBigcommerce.cli()
