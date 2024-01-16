"""Resolvers for the queries of the Products API"""
from ariadne import QueryType

from web.data import ingredients, products

query = QueryType()


@query.field("allIngredients")
def resolve_all_ingredients(*_):
    return ingredients


@query.field("allProducts")
def resolve_all_products(*_):
    return products


@query.field("products")
def resolve_products(*_, input=None):
    result_set = [product for product in products]
    if input is None:
        return result_set

    result_set = [
        product
        for product in result_set
        if product["available"] is input["available"]
    ]

    if input.get("minPrice") is not None:
        result_set = [
            product
            for product in result_set
            if product["price"] >= input["minPrice"]
        ]

    if input.get("maxPrice") is not None:
        result_set = [
            product
            for product in result_set
            if product["price"] <= input["maxPrice"]
        ]

    result_set.sort(
        key=lambda product: product.get(input["sortBy"], 0),
        reverse=input["sort"] == "DESCENDING",
    )
    # we ignore the pagination for now
    return result_set
