"""Resolver for object types, custom scalar types, and object properties"""

from datetime import datetime

from ariadne import ScalarType, UnionType

product_type = UnionType("Product")
datetime_scalar = ScalarType("Datetime")


@product_type.type_resolver
def resolve_product_type(obj, *_):
    if "hasFilling" in obj:
        return "Cake"
    else:
        return "Beverage"


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


@datetime_scalar.value_parser
def parse_datetime_value(value):
    return datetime.fromisoformat(value)
