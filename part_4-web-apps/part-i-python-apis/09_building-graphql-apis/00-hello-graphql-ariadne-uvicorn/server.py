"""Hello, world GraphQL server using Ariadne"""
import random
import string

from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL

schema = """
type Query {
    hello: String
}
"""

query = QueryType()

@query.field("hello")
def resolve_hello(*_):
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


server = GraphQL(make_executable_schema(schema, [query]), debug=True)
