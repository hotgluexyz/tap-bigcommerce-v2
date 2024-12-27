"""Stream type classes for tap-bigcommerce."""

from requests.models import Response as Response
from singer_sdk import typing as th
from typing import Optional

from tap_bigcommerce.client_v2 import BigcommerceV2Stream
from tap_bigcommerce.client_v3 import BigcommerceV3Stream


class CategoriesStream(BigcommerceV3Stream):
    name = "categories"
    path = "/v3/catalog/trees/categories"
    primary_keys = ["category_id"]
    records_jsonpath = "$.data[*]"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("category_id", th.IntegerType),
        th.Property("parent_id", th.IntegerType),
        th.Property("tree_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("description", th.StringType),
        th.Property("views", th.IntegerType),
        th.Property(
            "sort_order",
            th.IntegerType,
        ),
        th.Property("page_title", th.StringType),
        th.Property("search_keywords", th.StringType),
        th.Property("meta_keywords", th.ArrayType(th.StringType)),
        th.Property("meta_description", th.StringType),
        th.Property("layout_file", th.StringType),
        th.Property("is_visible", th.BooleanType),
        th.Property("default_product_sort", th.StringType),
        th.Property(
            "url",
            th.ObjectType(
                th.Property("path", th.StringType),
                th.Property("is_customized", th.BooleanType),
            ),
        ),
        th.Property("image_url", th.StringType),
    ).to_dict()


class CouponsStream(BigcommerceV2Stream):
    name = "coupons"
    path = "/v2/coupons"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("type", th.StringType),
        th.Property("amount", th.StringType),
        th.Property("min_purchase", th.StringType),
        th.Property("expires", th.StringType),
        th.Property("enabled", th.BooleanType),
        th.Property("code", th.StringType),
        th.Property(
            "applies_to",
            th.ObjectType(
                th.Property("entity", th.StringType),
                th.Property("ids", th.ArrayType(th.IntegerType)),
            ),
        ),
        th.Property("num_uses", th.IntegerType),
        th.Property("max_uses", th.IntegerType),
        th.Property("max_uses_per_customer", th.IntegerType),
        th.Property("restricted_to", th.CustomType({"type": ["array", "string"]})),
        th.Property("shipping_methods", th.ArrayType(th.StringType)),
        th.Property("date_created", th.DateTimeType),
    ).to_dict()


class CustomersStream(BigcommerceV3Stream):
    name = "customers"
    path = "/v3/customers"
    primary_keys = ["id"]
    records_jsonpath = "$.data[*]"
    replication_key = "date_modified"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property(
            "authentication",
            th.ObjectType(
                th.Property("force_password_reset", th.BooleanType),
            ),
        ),
        th.Property("company", th.StringType),
        th.Property("customer_group_id", th.IntegerType),
        th.Property("email", th.StringType),
        th.Property("first_name", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property("notes", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("registration_ip_address", th.StringType),
        th.Property("tax_exempt_category", th.StringType),
        th.Property("date_created", th.DateTimeType),
        th.Property("date_modified", th.DateTimeType),
        th.Property("accepts_product_review_abandoned_cart_emails", th.BooleanType),
        th.Property("channel_ids", th.ArrayType(th.IntegerType)),
        th.Property(
            "addresses",
            th.ArrayType(
                th.ObjectType(
                    th.Property("first_name", th.StringType),
                    th.Property("last_name", th.StringType),
                    th.Property("address1", th.StringType),
                    th.Property("address2", th.StringType),
                    th.Property("city", th.StringType),
                    th.Property("state_or_province", th.StringType),
                    th.Property("postal_code", th.StringType),
                    th.Property("country_code", th.StringType),
                    th.Property("phone", th.StringType),
                    th.Property("address_type", th.StringType),
                    th.Property("customer_id", th.IntegerType),
                    th.Property("id", th.IntegerType),
                    th.Property("country", th.StringType),
                )
            ),
        ),
        th.Property(
            "store_credit_amounts",
            th.ArrayType(
                th.ObjectType(
                    th.Property("amount", th.NumberType),
                )
            ),
        ),
        th.Property("shopper_profile_id", th.StringType),
        th.Property("segment_ids", th.ArrayType(th.StringType)),
    ).to_dict()

def get_orders_schema():
    return th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("customer_id", th.IntegerType),
        th.Property("date_created", th.DateTimeType),
        th.Property("date_modified", th.DateTimeType),
        th.Property("date_shipped", th.DateTimeType),
        th.Property("status_id", th.IntegerType),
        th.Property("status", th.StringType),
        th.Property("subtotal_ex_tax", th.StringType),
        th.Property("subtotal_inc_tax", th.StringType),
        th.Property("subtotal_tax", th.StringType),
        th.Property("base_shipping_cost", th.StringType),
        th.Property("shipping_cost_ex_tax", th.StringType),
        th.Property("shipping_cost_inc_tax", th.StringType),
        th.Property("shipping_cost_tax", th.StringType),
        th.Property("shipping_cost_tax_class_id", th.IntegerType),
        th.Property("base_handling_cost", th.StringType),
        th.Property("handling_cost_ex_tax", th.StringType),
        th.Property("handling_cost_inc_tax", th.StringType),
        th.Property("handling_cost_tax", th.StringType),
        th.Property("handling_cost_tax_class_id", th.IntegerType),
        th.Property("base_wrapping_cost", th.StringType),
        th.Property("wrapping_cost_ex_tax", th.StringType),
        th.Property("wrapping_cost_inc_tax", th.StringType),
        th.Property("wrapping_cost_tax", th.StringType),
        th.Property("wrapping_cost_tax_class_id", th.IntegerType),
        th.Property("total_ex_tax", th.StringType),
        th.Property("total_inc_tax", th.StringType),
        th.Property("total_tax", th.StringType),
        th.Property("items_total", th.IntegerType),
        th.Property("items_shipped", th.IntegerType),
        th.Property("payment_method", th.StringType),
        th.Property("payment_provider_id", th.StringType),
        th.Property("payment_status", th.StringType),
        th.Property("refunded_amount", th.StringType),
        th.Property("order_is_digital", th.BooleanType),
        th.Property("store_credit_amount", th.StringType),
        th.Property("gift_certificate_amount", th.StringType),
        th.Property("ip_address", th.StringType),
        th.Property("ip_address_v6", th.StringType),
        th.Property("geoip_country", th.StringType),
        th.Property("geoip_country_iso2", th.StringType),
        th.Property("currency_id", th.IntegerType),
        th.Property("currency_code", th.StringType),
        th.Property("currency_exchange_rate", th.StringType),
        th.Property("default_currency_id", th.IntegerType),
        th.Property("default_currency_code", th.StringType),
        th.Property("staff_notes", th.StringType),
        th.Property("customer_message", th.StringType),
        th.Property("discount_amount", th.StringType),
        th.Property("coupon_discount", th.StringType),
        th.Property("shipping_address_count", th.IntegerType),
        th.Property("is_deleted", th.BooleanType),
        th.Property("ebay_order_id", th.StringType),
        th.Property("cart_id", th.StringType),
        th.Property(
            "billing_address",
            th.ObjectType(
                th.Property("first_name", th.StringType),
                th.Property("last_name", th.StringType),
                th.Property("company", th.StringType),
                th.Property("street_1", th.StringType),
                th.Property("street_2", th.StringType),
                th.Property("city", th.StringType),
                th.Property("state", th.StringType),
                th.Property("zip", th.StringType),
                th.Property("country", th.StringType),
                th.Property("country_iso2", th.StringType),
                th.Property("phone", th.StringType),
                th.Property("email", th.StringType),
                th.Property("form_fields", th.CustomType({"type": ["array", "string"]})),
            ),
        ),
        th.Property("is_email_opt_in", th.BooleanType),
        th.Property("credit_card_type", th.StringType),
        th.Property("order_source", th.StringType),
        th.Property("channel_id", th.IntegerType),
        th.Property("external_source", th.StringType),
        th.Property(
            "products",
            th.ObjectType(
                th.Property("url", th.StringType),
                th.Property("resource", th.StringType),
            ),
        ),
        th.Property(
            "shipping_addresses",
            th.ObjectType(
                th.Property("url", th.StringType),
                th.Property("resource", th.StringType),
            ),
        ),
        th.Property(
            "coupons",
            th.ObjectType(
                th.Property("url", th.StringType),
                th.Property("resource", th.StringType),
            ),
        ),
        th.Property("external_id", th.StringType),
        th.Property("external_merchant_id", th.CustomType({"type": ["array", "string"]})),
        th.Property("tax_provider_id", th.StringType),
        th.Property("customer_locale", th.StringType),
        th.Property("external_order_id", th.StringType),
        th.Property("store_default_currency_code", th.StringType),
        th.Property("store_default_to_transactional_exchange_rate", th.StringType),
        th.Property("custom_status", th.StringType),
    ).to_dict()


class OrdersStream(BigcommerceV2Stream):
    name = "orders"
    path = "/v2/orders"
    primary_keys = ["id"]
    replication_key = "date_modified"
    schema = get_orders_schema()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "order_products_path": record["products"]["resource"],
            "order_id": record["id"],
        }

def get_order_lines_schema():
    return th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("order_id", th.IntegerType),
        th.Property("product_id", th.IntegerType),
        th.Property("variant_id", th.IntegerType),
        th.Property("order_address_id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("name_customer", th.StringType),
        th.Property("name_merchant", th.StringType),
        th.Property("sku", th.StringType),
        th.Property("upc", th.StringType),
        th.Property("type", th.StringType),
        th.Property("base_price", th.StringType),
        th.Property("price_ex_tax", th.StringType),
        th.Property("price_inc_tax", th.StringType),
        th.Property("price_tax", th.StringType),
        th.Property("base_total", th.StringType),
        th.Property("total_ex_tax", th.StringType),
        th.Property("total_inc_tax", th.StringType),
        th.Property("total_tax", th.StringType),
        th.Property("weight", th.StringType),
        th.Property("width", th.StringType),
        th.Property("height", th.StringType),
        th.Property("depth", th.StringType),
        th.Property("quantity", th.IntegerType),
        th.Property("base_cost_price", th.StringType),
        th.Property("cost_price_inc_tax", th.StringType),
        th.Property("cost_price_ex_tax", th.StringType),
        th.Property("cost_price_tax", th.StringType),
        th.Property("is_refunded", th.BooleanType),
        th.Property("quantity_refunded", th.IntegerType),
        th.Property("refund_amount", th.StringType),
        th.Property("return_id", th.IntegerType),
        th.Property("wrapping_id", th.IntegerType),
        th.Property("wrapping_name", th.StringType),
        th.Property("base_wrapping_cost", th.StringType),
        th.Property("wrapping_cost_ex_tax", th.StringType),
        th.Property("wrapping_cost_inc_tax", th.StringType),
        th.Property("wrapping_cost_tax", th.StringType),
        th.Property("wrapping_message", th.StringType),
        th.Property("quantity_shipped", th.IntegerType),
        th.Property("event_name", th.StringType),
        th.Property("event_date", th.DateTimeType),
        th.Property("fixed_shipping_cost", th.StringType),
        th.Property("ebay_item_id", th.StringType),
        th.Property("ebay_transaction_id", th.StringType),
        th.Property("option_set_id", th.IntegerType),
        th.Property("parent_order_product_id", th.IntegerType),
        th.Property("is_bundled_product", th.BooleanType),
        th.Property("bin_picking_number", th.StringType),
        th.Property("external_id", th.StringType),
        th.Property("fulfillment_source", th.StringType),
        th.Property("brand", th.StringType),
        th.Property("gift_certificate_id", th.CustomType({"type": ["number", "string"]})),
        th.Property("applied_discounts", th.ArrayType(
            th.ObjectType(
                th.Property("id", th.StringType),
                th.Property("amount", th.StringType),
                th.Property("name", th.StringType),
                th.Property("code", th.StringType),
                th.Property("target", th.StringType),
            )
        )),
        th.Property("product_options", th.ArrayType(
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("option_id", th.IntegerType),
                th.Property("order_product_id", th.IntegerType),
                th.Property("product_option_id", th.IntegerType),
                th.Property("display_name", th.StringType),
                th.Property("display_name_customer", th.StringType),
                th.Property("display_name_merchant", th.StringType),
                th.Property("display_value", th.StringType),
                th.Property("display_value_customer", th.StringType),
                th.Property("display_value_merchant", th.StringType),
                th.Property("value", th.StringType),
                th.Property("type", th.StringType),
                th.Property("name", th.StringType),
                th.Property("display_style", th.StringType),
            )
        )),
    ).to_dict()

class OrderLinesStream(BigcommerceV2Stream):
    name = "order_lines"
    path = "/v2{order_products_path}"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = OrdersStream
    schema = get_order_lines_schema()


class ProductsStream(BigcommerceV3Stream):
    name = "products"
    path = "/v3/catalog/products"
    primary_keys = ["id"]
    records_jsonpath = "$.data[*]"
    replication_key = "date_modified"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("type", th.StringType),
        th.Property("sku", th.StringType),
        th.Property("description", th.StringType),
        th.Property("weight", th.NumberType),
        th.Property("width", th.NumberType),
        th.Property("depth", th.NumberType),
        th.Property("height", th.NumberType),
        th.Property("price", th.NumberType),
        th.Property("cost_price", th.NumberType),
        th.Property("retail_price", th.NumberType),
        th.Property("sale_price", th.NumberType),
        th.Property("map_price", th.NumberType),
        th.Property("tax_class_id", th.IntegerType),
        th.Property("product_tax_code", th.StringType),
        th.Property("calculated_price", th.NumberType),
        th.Property("categories", th.ArrayType(th.IntegerType)),
        th.Property("brand_id", th.IntegerType),
        th.Property("option_set_id", th.IntegerType),
        th.Property("option_set_display", th.StringType),
        th.Property("inventory_level", th.IntegerType),
        th.Property("inventory_warning_level", th.IntegerType),
        th.Property("inventory_tracking", th.StringType),
        th.Property("reviews_rating_sum", th.IntegerType),
        th.Property("reviews_count", th.IntegerType),
        th.Property("total_sold", th.IntegerType),
        th.Property("fixed_cost_shipping_price", th.NumberType),
        th.Property("is_free_shipping", th.BooleanType),
        th.Property("is_visible", th.BooleanType),
        th.Property("is_featured", th.BooleanType),
        th.Property("related_products", th.ArrayType(th.IntegerType)),
        th.Property("warranty", th.StringType),
        th.Property("bin_picking_number", th.StringType),
        th.Property("layout_file", th.StringType),
        th.Property("upc", th.StringType),
        th.Property("mpn", th.StringType),
        th.Property("gtin", th.StringType),
        th.Property("search_keywords", th.StringType),
        th.Property("availability_description", th.StringType),
        th.Property("availability", th.StringType),
        th.Property("gift_wrapping_options_type", th.StringType),
        th.Property("gift_wrapping_options_list", th.ArrayType(th.StringType)),
        th.Property("sort_order", th.IntegerType),
        th.Property("condition", th.StringType),
        th.Property("is_condition_shown", th.BooleanType),
        th.Property("order_quantity_minimum", th.IntegerType),
        th.Property("order_quantity_maximum", th.IntegerType),
        th.Property("page_title", th.StringType),
        th.Property("meta_keywords", th.ArrayType(th.StringType)),
        th.Property("meta_description", th.StringType),
        th.Property("date_created", th.DateTimeType),
        th.Property("date_modified", th.DateTimeType),
        th.Property("view_count", th.IntegerType),
        th.Property("preorder_release_date", th.DateTimeType),
        th.Property("preorder_message", th.StringType),
        th.Property("is_preorder_only", th.BooleanType),
        th.Property("is_price_hidden", th.BooleanType),
        th.Property("price_hidden_label", th.StringType),
        th.Property(
            "custom_url",
            th.ObjectType(
                th.Property("url", th.StringType),
                th.Property("is_customized", th.BooleanType),
            ),
        ),
        th.Property("base_variant_id", th.IntegerType),
        th.Property("open_graph_type", th.StringType),
        th.Property("open_graph_title", th.StringType),
        th.Property("open_graph_description", th.StringType),
        th.Property("open_graph_use_meta_description", th.BooleanType),
        th.Property("open_graph_use_product_name", th.BooleanType),
        th.Property("open_graph_use_image", th.BooleanType)
    ).to_dict()

    def get_child_context(self, record, context):
        return {
            "product_id": record["id"],
        }


class VariantsStream(BigcommerceV3Stream):
    name = "variants"
    path = "/v3/catalog/variants"
    primary_keys = ["id"]
    records_jsonpath = "$.data[*]"
    replication_key = None
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("product_id", th.IntegerType),
        th.Property("sku", th.StringType),
        th.Property("sku_id", th.IntegerType),
        th.Property("price", th.NumberType),
        th.Property("calculated_price", th.NumberType),
        th.Property("sale_price", th.NumberType),
        th.Property("retail_price", th.NumberType),
        th.Property("map_price", th.NumberType),
        th.Property("weight", th.NumberType),
        th.Property("calculated_weight", th.NumberType),
        th.Property("width", th.NumberType),
        th.Property("height", th.NumberType),
        th.Property("depth", th.NumberType),
        th.Property("is_free_shipping", th.BooleanType),
        th.Property("fixed_cost_shipping_price", th.NumberType),
        th.Property("purchasing_disabled", th.BooleanType),
        th.Property("purchasing_disabled_message", th.StringType),
        th.Property("image_url", th.StringType),
        th.Property("cost_price", th.NumberType),
        th.Property("upc", th.StringType),
        th.Property("mpn", th.StringType),
        th.Property("gtin", th.StringType),
        th.Property("inventory_level", th.IntegerType),
        th.Property("inventory_warning_level", th.IntegerType),
        th.Property("bin_picking_number", th.StringType),
        th.Property("option_values", th.ArrayType(
            th.ObjectType(
                th.Property("id", th.NumberType),
                th.Property("label", th.StringType),
                th.Property("option_id", th.NumberType),
                th.Property("option_display_name", th.StringType),
            )
        ))
    ).to_dict()


class RefundsStream(BigcommerceV3Stream):
    name = "refunds"
    path = "/v3/orders/payment_actions/refunds"
    primary_keys = ["order_id"]
    records_jsonpath = "$.data[*]"
    replication_key = "created"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("order_id", th.IntegerType),
        th.Property("user_id", th.IntegerType),
        th.Property("created", th.DateTimeType),
        th.Property("reason", th.StringType),
        th.Property("total_amount", th.NumberType),
        th.Property("total_tax", th.NumberType),
        th.Property("uses_merchant_override_values", th.BooleanType),
        th.Property("items", th.ArrayType(
            th.ObjectType(
                th.Property("item_type", th.StringType),
                th.Property("item_id", th.NumberType),
                th.Property("quantity", th.NumberType),
                th.Property("requested_amount", th.NumberType),
                th.Property("reason", th.StringType),
                th.Property("adjustments", th.ArrayType(
                    th.ObjectType(
                        th.Property("amount", th.NumberType),
                        th.Property("description", th.StringType),
                    )
                ))
            )
        )),
        th.Property("payments", th.ArrayType(
            th.ObjectType(
                th.Property("id", th.IntegerType),
                th.Property("provider_id", th.StringType),
                th.Property("amount", th.NumberType),
                th.Property("offline", th.BooleanType),
                th.Property("is_declined", th.BooleanType),
                th.Property("declined_message", th.StringType),
                th.Property("transaction_id", th.StringType),
            )
        )),
        th.Property("store_hash", th.StringType),
    ).to_dict()
    
    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        row["store_hash"] = self.config.get("store_hash")
        return row

    def get_child_context(self, record, context):
        return {
            "order_id": record["order_id"],
        }


class RefundOrderStream(BigcommerceV2Stream):
    name = "refund_order"
    path = "/v2/orders/{order_id}"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = RefundsStream
    schema = get_orders_schema()
    orders_synced = []
    
    def get_next_page_token(self, response, previous_token):
        return None
    
    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "order_products_path": record["products"]["resource"],
            "order_id": record["id"],
        }
        
    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        if row["id"] not in self.orders_synced:
            self.orders_synced.append(row["id"])
            return row
        else:
            return None
        
class RefundOrderItemsStream(BigcommerceV2Stream):
    name = "refund_order_items"
    path = "/v2{order_products_path}"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = RefundOrderStream
    schema = get_order_lines_schema()

class OrderShippingAddressStream(BigcommerceV3Stream):
    name = "order_shipping_addresses"
    path = "/v2/orders/{order_id}/shipping_addresses"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = OrdersStream
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("order_id", th.IntegerType),
        th.Property("first_name", th.StringType),
        th.Property("last_name", th.StringType),
        th.Property("company", th.StringType),
        th.Property("street_1", th.StringType),
        th.Property("street_2", th.StringType),
        th.Property("city", th.StringType),
        th.Property("zip", th.StringType),
        th.Property("country", th.StringType),
        th.Property("country_iso2", th.StringType),
        th.Property("state", th.StringType),
        th.Property("email", th.StringType),
        th.Property("phone", th.StringType),
        th.Property("items_total", th.NumberType),
        th.Property("items_shipped", th.NumberType),
        th.Property("shipping_method", th.StringType),
        th.Property("base_cost", th.StringType),
        th.Property("cost_ex_tax", th.StringType),
        th.Property("cost_inc_tax", th.StringType),
        th.Property("cost_tax", th.StringType),
        th.Property("cost_tax_class_id", th.NumberType),
        th.Property("base_handling_cost", th.StringType),
        th.Property("handling_cost_ex_tax", th.StringType),
        th.Property("handling_cost_inc_tax", th.StringType),
        th.Property("handling_cost_tax", th.StringType),
        th.Property("handling_cost_tax_class_id", th.NumberType),
        th.Property("shipping_zone_id", th.NumberType),
        th.Property("shipping_zone_name", th.StringType),
        th.Property("shipping_quotes", th.CustomType({"type": ["object", "string"]})),
        th.Property("form_fields", th.CustomType({"type": ["array", "string"]})),
    ).to_dict()


class OrderConsignmentsStream(BigcommerceV2Stream):
    name = "order_consignments"
    path = "/v2/orders/{order_id}/consignments"
    replication_key = None
    parent_stream_type = OrdersStream
    schema = th.PropertiesList(
        th.Property("pickups", th.CustomType({"type": ["array", "string"]})),
        th.Property("shipping", th.CustomType({"type": ["array", "string"]})),
        th.Property("downloads", th.CustomType({"type": ["array", "string"]})),
        th.Property("email", th.CustomType({"type": ["object", "string"]})),
        th.Property("order_id", th.IntegerType),
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        row["order_id"] = context.get("order_id")
        return row

    def get_next_page_token(self, response, previous_token):
        return None


class ProductImagesStream(BigcommerceV3Stream):
    name = "product_images"
    path = "/v3/catalog/products/{product_id}/images"
    primary_keys = ["id"]
    replication_key = None
    parent_stream_type = ProductsStream

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("product_id", th.IntegerType),
        th.Property("image_file", th.StringType),
        th.Property("url_zoom", th.StringType),
        th.Property("url_standard", th.StringType),
        th.Property("url_thumbnail", th.StringType),
        th.Property("url_tiny", th.StringType),
        th.Property("date_modified", th.DateTimeType)
    ).to_dict()

    def parse_response(self, response):
        yield from response.json()["data"]


class TransactionsStream(BigcommerceV2Stream):
    name = "transactions"
    path = "/v3/orders/{order_id}/transactions"
    replication_key = None
    parent_stream_type = RefundOrderStream
    records_jsonpath = "$.data[*]"
    schema = th.PropertiesList(
        th.Property("order_id", th.IntegerType),
        th.Property("event", th.StringType),
        th.Property("method", th.StringType),
        th.Property("amount", th.NumberType),
        th.Property("currency", th.StringType),
        th.Property("gateway", th.StringType),
        th.Property("gateway_transaction_id", th.StringType),
        th.Property("test", th.BooleanType),
        th.Property("status", th.StringType),
        th.Property("fraud_review", th.BooleanType),
        th.Property("reference_transaction_id", th.IntegerType),
        th.Property("offline", th.ObjectType(
                th.Property("display_name", th.StringType),
            )),
        th.Property("custom", th.ObjectType(
                th.Property("payment_method", th.StringType),
            )),
        th.Property("payment_method_id", th.StringType),
        th.Property("id", th.IntegerType),
        th.Property("date_created", th.DateTimeType),
        th.Property("payment_instrument_token", th.StringType),
        th.Property("avs_result", th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("message", th.StringType),
                th.Property("street_match", th.StringType),
                th.Property("postal_match", th.StringType),
            )),
        th.Property("cvv_result", th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("message", th.StringType),
            )),
        th.Property("credit_card", th.ObjectType(
                th.Property("card_type", th.StringType),
                th.Property("card_iin", th.StringType),
                th.Property("card_last4", th.StringType),
                th.Property("card_expiry_month", th.IntegerType),
                th.Property("card_expiry_year", th.IntegerType),
            )),
        th.Property("gift_certificate", th.ObjectType(
                th.Property("code", th.StringType),
                th.Property("original_balance", th.NumberType),
                th.Property("starting_balance", th.NumberType),
                th.Property("remaining_balance", th.NumberType),
                th.Property("status", th.StringType),
            )),
        th.Property("store_credit", th.ObjectType(
                th.Property("remaining_balance", th.NumberType),
            )),
        th.Property("custom_provider_field_result", th.ObjectType(
                th.Property("receipt_number", th.StringType),
                th.Property("authorization_code", th.StringType),
                th.Property("fraud_response", th.StringType),
                th.Property("amount_received", th.NumberType),
            )),
    ).to_dict()

    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        row["order_id"] = context.get("order_id")
        return row

    def get_next_page_token(self, response, previous_token):
        return None