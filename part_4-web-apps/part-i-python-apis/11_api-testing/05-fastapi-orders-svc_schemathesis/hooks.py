"""Implementation of Dredd hooks for endpoint testing"""
import json
import logging

import dredd_hooks
import requests

logger = logging.getLogger()

# Global object to store and manage the state of the test suite
response_stash = {}

@dredd_hooks.before_all
def print_something(transactions):
    print("Something!")
    logger.error("Something something!")

@dredd_hooks.after("/orders > Creates an order > 201 > application/json")
def save_created_order(transaction):
    response_payload = transaction["real"]["body"]
    order_id = json.loads(response_payload)["id"]
    response_stash["created_order_id"] = order_id


@dredd_hooks.before(
    "/orders/{order_id} > Returns the details of a specific order > 200 > application/json"  # pylint: disable=C0301:line-too-long
)
def inject_order_id_before_get_order(transaction):
    transaction["fullPath"] = f"/orders/{response_stash['created_order_id']}"
    transaction["request"][
        "uri"
    ] = f"/orders/{response_stash['created_order_id']}"


@dredd_hooks.before(
    "/orders/{order_id} > Replaces an existing order > 200 > application/json"
)
def inject_order_id_before_put_order(transaction):
    transaction["fullPath"] = f"/orders/{response_stash['created_order_id']}"
    transaction["request"][
        "uri"
    ] = f"/orders/{response_stash['created_order_id']}"


@dredd_hooks.before("/orders/{order_id} > Deletes an existing order > 204")
def inject_order_id_before_delete_order(transaction):
    transaction["fullPath"] = f"/orders/{response_stash['created_order_id']}"
    transaction["request"][
        "uri"
    ] = f"/orders/{response_stash['created_order_id']}"


@dredd_hooks.before(
    "/orders/{order_id}/pay > Processes payment for an order > 200 > application/json"  # pylint: disable=C0301:line-too-long
)
def before_pay_order(transaction):
    logger.error("**************************************************** here!")
    response = requests.post(
        "http://localhost:8080/orders",
        json={"order": [{"product": "string", "size": "small", "quantity": 1}]},
        timeout=10,
    )
    id_ = response.json()["id"]
    transaction["fullPath"] = f"/orders/{id_}/pay"
    transaction["request"]["uri"] = f"/orders/{id_}/pay"


@dredd_hooks.before(
    "/orders/{order_id}/cancel > Cancels an order > 200 > application/json"
)
def before_cancel_order(transaction):
    response = requests.post(
        "http://localhost:8080/orders",
        json={"order": [{"product": "string", "size": "small", "quantity": 1}]},
        timeout=10,
    )
    id_ = response.json()["id"]
    transaction["fullPath"] = f"/orders/{id_}/cancel"
    transaction["request"]["uri"] = f"/orders/{id_}/cancel"


@dredd_hooks.before("/orders > Creates an order > 422 > application/json")
def inject_invalid_payload_create_order(transaction):
    transaction["request"]["body"] = json.dumps(
        {"order": [{"product": "string", "size": "qwerty"}]}
    )


@dredd_hooks.before(
    "/orders/{order_id} > Returns the details of a specific order > 422 > application/json"  # pylint: disable=C0301:line-too-long
)
@dredd_hooks.before(
    "/orders/{order_id}/cancel > Cancels an order > 422 > application/json"
)
@dredd_hooks.before(
    "/orders/{order_id}/pay > Processes payment for an order > 422 > application/json"  # pylint: disable=C0301:line-too-long
)
@dredd_hooks.before(
    "/orders/{order_id} > Replaces an existing order > 422 > application/json"
)
@dredd_hooks.before(
    "/orders/{order_id} > Deletes an existing order > 422 > application/json"
)
def inject_invalid_order_id_format(transaction):
    transaction["fullPath"] = transaction["fullPath"].replace(
        "12791611-2d52-47c5-9cec-d97c181cc3ed", "55"
    )
    transaction["request"]["uri"] = transaction["request"]["uri"].replace(
        "12791611-2d52-47c5-9cec-d97c181cc3ed", "55"
    )


@dredd_hooks.before(
    "/orders > Returns a list of orders > 422 > application/json"
)
def inject_invalid_query_params(transaction):
    logger.error("%s Injection of /orders > 422", "=" * 40)
    print("*" * 40, "injection!")
    if "?" in transaction["fullPath"]:
        transaction["fullPath"] = "".join(
            [transaction["fullPath"], "&", "cancelled=maybe"]
        )
    else:
        transaction["fullPath"] = "".join(
            [transaction["fullPath"], "?", "cancelled=maybe"]
        )
