"""Resolvers for the queries of the Products API"""
from ariadne import QueryType

from web.data import ingredients

query = QueryType()

@query.field("allIngredients")
def resolve_all_ingredients(*_):
    return ingredients
