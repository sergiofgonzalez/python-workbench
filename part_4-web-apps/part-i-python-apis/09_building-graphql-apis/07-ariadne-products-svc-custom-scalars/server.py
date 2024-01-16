"""Entry-point for the Products service which exposes a GraphQL API"""
from ariadne.asgi import GraphQL

from web.schema import schema

server = GraphQL(schema, debug=True)
