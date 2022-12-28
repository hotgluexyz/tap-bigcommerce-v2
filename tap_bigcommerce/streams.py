"""Stream type classes for tap-bigcommerce."""

from singer_sdk import typing as th

from tap_bigcommerce.client_v2 import BigcommerceV2Stream
from tap_bigcommerce.client_v3 import BigcommerceV3Stream


class CategoriesStream(BigcommerceV3Stream):
    """Define custom stream."""

    name = "categories"
    path = "/v3/catalog/trees/categories"
    primary_keys = ["id"]
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
    """Define custom stream."""

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
        th.Property("restricted_to", th.ObjectType()),
        th.Property("shipping_methods", th.ArrayType(th.StringType)),
        th.Property("date_created", th.DateTimeType),
    ).to_dict()


class CustomersStream(BigcommerceV3Stream):
    """Define custom stream."""

    name = "customers"
    path = "/v3/customers"
    primary_keys = ["id"]
    records_jsonpath = "$.data[*]"
    replication_key = "date_modified"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
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


class OrdersStream(BigcommerceV2Stream):
    """Define custom stream."""

    name = "orders"
    path = "/v2/orders"
    primary_keys = ["id"]
    replication_key = "date_modified"
    schema = th.PropertiesList(
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
                th.Property("form_fields", th.ArrayType(th.StringType)),
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
        th.Property("external_merchant_id", th.ObjectType()),
        th.Property("tax_provider_id", th.StringType),
        th.Property("customer_locale", th.StringType),
        th.Property("external_order_id", th.StringType),
        th.Property("store_default_currency_code", th.StringType),
        th.Property("store_default_to_transactional_exchange_rate", th.StringType),
        th.Property("custom_status", th.StringType),
    ).to_dict()


class ProductsStream(BigcommerceV3Stream):
    """Define custom stream."""

    name = "products"
    path = "/v3/catalog/products"
    primary_keys = ["id"]
    records_jsonpath = "$.data[*]"
    replication_key = "date_modified"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.IntegerType),
        th.Property("type", th.DateTimeType),
        th.Property("sku", th.DateTimeType),
        th.Property("description", th.DateTimeType),
        th.Property("weight", th.IntegerType),
        th.Property("width", th.IntegerType),
        th.Property("depth", th.IntegerType),
        th.Property("height", th.IntegerType),
        th.Property("price", th.IntegerType),
        th.Property("cost_price", th.IntegerType),
        th.Property("retail_price", th.IntegerType),
        th.Property("sale_price", th.IntegerType),
        th.Property("map_price", th.IntegerType),
        th.Property("tax_class_id", th.IntegerType),
        th.Property("product_tax_code", th.StringType),
        th.Property("calculated_price", th.IntegerType),
        th.Property("categories", th.ArrayType(th.IntegerType)),
        th.Property("brand_id", th.IntegerType),
        th.Property("option_set_id", th.IntegerType),
        th.Property("option_set_display", th.StringType),
        th.Property("inventory_level", th.IntegerType),
        th.Property("inventory_warning_level", th.IntegerType),
        th.Property("inventory_tracking", th.IntegerType),
        th.Property("reviews_rating_sum", th.IntegerType),
        th.Property("reviews_count", th.IntegerType),
        th.Property("total_sold", th.IntegerType),
        th.Property("fixed_cost_shipping_price", th.IntegerType),
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
        th.Property("gift_wrapping_options_list", th.ArrayType(th.IntegerType)),
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
        th.Property("base_variant_id", th.StringType),
        th.Property("open_graph_type", th.StringType),
        th.Property("open_graph_title", th.StringType),
        th.Property("open_graph_description", th.StringType),
        th.Property("open_graph_use_meta_description", th.BooleanType),
        th.Property("open_graph_use_product_name", th.BooleanType),
        th.Property("open_graph_use_image", th.BooleanType),
    ).to_dict()
