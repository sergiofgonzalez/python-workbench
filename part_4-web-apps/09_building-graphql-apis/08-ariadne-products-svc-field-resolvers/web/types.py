"""Resolver for object types, custom scalar types, and object properties"""

import copy
from datetime import datetime

from ariadne import InterfaceType, ScalarType, UnionType

from web.data import ingredients

product_type = UnionType("Product")
datetime_scalar = ScalarType("Datetime")
product_interface = InterfaceType("ProductInterface")


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


@product_interface.field("ingredients")
def resolve_product_ingredients(product, _):
    ingredient_recipes = [
        copy.copy(ingredient) for ingredient in product.get("ingredients", [])
    ]
    for ingredient_recipe in ingredient_recipes:
        for ingredient in ingredients:
            if ingredient["id"] == ingredient_recipe["ingredient"]:
                ingredient_recipe["ingredient"] = ingredient
    return ingredient_recipes
