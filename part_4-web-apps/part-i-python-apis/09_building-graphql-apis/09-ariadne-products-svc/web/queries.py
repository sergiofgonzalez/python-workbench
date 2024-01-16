"""Resolvers for the queries of the Products API"""
from itertools import islice

from ariadne import QueryType

from web.data import ingredients, products
from exceptions import ItemNotFoundError

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

    if input["available"] is not None:
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
    return get_page(result_set, input["resultsPerPage"], input["page"])


@query.field("product")
def resolve_product(*_, id):
    for product in products:
        if product["id"] == id:
            return product
    raise ItemNotFoundError(f"Product with ID {id} was not found")

@query.field("ingredient")
def resolve_ingredient(*_, id):
    for ingredient in ingredients:
        if ingredient["id"] == id:
            return ingredient
    raise ItemNotFoundError(f"Ingredient with ID {id} was not found")


def get_page(items, items_per_page, page):
    page = page - 1  # islice() uses zero-based indexing
    start = items_per_page * page if page > 0 else page
    stop = start + items_per_page
    return list(islice(items, start, stop))
