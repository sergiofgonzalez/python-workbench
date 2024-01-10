"""Simple `requests`-based GraphQL client for illustration purposes"""
import requests

# Using a GET request
URL = "http://localhost:9002/graphql"

query_doc = """
{
    allIngredients {
        name
    }
}
"""

response = requests.get(URL, params={"query": query_doc}, timeout=10)
print(f"status code: {response.status_code}\n{response.json()}")


# Using a POST request
response = requests.post(URL, json={"query": query_doc}, timeout=10)
print(f"status code: {response.status_code}\n{response.json()}")
