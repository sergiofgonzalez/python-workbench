"""Supporting code to load the executable schema"""
from pathlib import Path

from ariadne import make_executable_schema

from web.mutations import mutation
from web.queries import query
from web.types import (
    datetime_scalar,
    ingredient_type,
    product_interface,
    product_type,
    supplier_type,
)

schema = make_executable_schema(
    (Path(__file__).parent / "products.graphql").read_text(),
    [
        query,
        mutation,
        product_type,
        datetime_scalar,
        product_interface,
        ingredient_type,
        supplier_type,
    ],
)
