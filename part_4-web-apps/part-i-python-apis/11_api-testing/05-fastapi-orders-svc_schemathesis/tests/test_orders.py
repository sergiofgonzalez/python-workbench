"""Test file using Hypothesis"""
import unittest
from pathlib import Path

import hypothesis.strategies as st
import jsonschema
import yaml
from fastapi.testclient import TestClient
from hypothesis import Verbosity, given, settings
from jsonschema import RefResolver, ValidationError

from orders.app import app

# Load OpenAPI spec file
orders_api_spec = yaml.full_load(
    (Path(__file__).parent / "../oas.yaml").read_text()
)

# Locate the CreateOrderSchema JSONSchema definition
create_order_schema = orders_api_spec["components"]["schemas"][
    "CreateOrderSchema"
]

test_client = TestClient(app=app)

values_strategy = st.none() | st.booleans() | st.text() | st.integers()
order_item_strategy = st.fixed_dictionaries(
    {
        "product": values_strategy,
        "size": st.one_of(st.sampled_from(["small", "medium", "big"]))
        | values_strategy,
        "quantity": values_strategy,
    }
)
order_payload_strategy = st.fixed_dictionaries(
    {"order": st.lists(order_item_strategy)}
)


class TestOrderCreation(unittest.TestCase):
    """Tests the POST /orders endpoint"""

    @staticmethod
    def is_valid_payload(payload, schema):
        """
        Uses JSONSchema and the OpenAPI spec to check if the payload is valid
        """
        try:
            jsonschema.validate(
                payload,
                schema=schema,
                resolver=RefResolver("", orders_api_spec),
            )
        except ValidationError:
            return False
        else:
            return True

    @given(order_item_strategy)
    @settings(verbosity=Verbosity.verbose, max_examples=500)
    def test_orders(self, payload):
        response = test_client.post("/orders", json=payload)
        if TestOrderCreation.is_valid_payload(payload, create_order_schema):
            self.assertEqual(response.status_code, 201)
        else:
            self.assertEqual(response.status_code, 422)


if __name__ == "__main__":
    unittest.main()
