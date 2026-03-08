# API concepts
> misc API concepts with examples implemented using FastAPI

+ [Basic API concepts]

## Basic API concepts

Through messaging, you can send small chunks of data in pipelines among processes.

These messages may be verb-like commands, or may just be noun-like events of interests.

### Communication patterns

Communication when using messages can accommodate these different patterns:

+ Request-Response: 1:1, like a browser calling a web server.
+ Publish-Subscribe: a publisher emits a messages and subscribers act on each according to some data in the message.
+ Queues: a publisher emits a message but only one out of a pool of subscriber grabs the message and acts on it.

### API specification concepts

A **resource** is data that you can distinguish and perform operations on.

An **endpoint** is a distinct URL and HTTP verb (i.e., action) a web service provides for each feature you want to expose. An endpoint is sometimes called a route, because the endpoint routes the URL to a function (path operation) that performs some logic.

There is a standard format for documenting REST APIs called **OpenAPI specification**.

Let's assume you are building an application that allows customers to order coffee.

The first step to you need to take to specify the API is to identify the URL paths and identify the capabilities each path will implement:

+ `/orders/`
    + `GET`: retrieve a list of orders.
    + `POST`: place an order.
+ `/orders/{order_id}`
    + `GET`: return an order by id.
    + `PUT`: update an order by id.
    + `DELETE`: delete an order by id.
+ `/orders/{order_id}/cancel`
    + `POST`: cancel an order.
+ `/orders/{order_id}/pay`
    + `POST`: pay an order.


The specification must also include the data models (i.e., models) describing the shape and characteristics of the data exchanged over those endpoints. The OpenAPI includes a section for those definitions (called schemas) of the data sent and received by your API. Those are written using the JSON schema standard for JSON data schema definitions.

It's common to name the model after the operation they support (e.g., `ItemCreate`, `OrderItem`, etc.). When writing the data model manually, the JSON schema specification for the model uses to order an item will look like the following:

```yaml
  schemas:
...
    OrderItemSchema:
      type: object
      required:
        - product
        - size
      properties:
        product:
          type: string
        size:
          type: string
          enum:
            - small
            - medium
            - big
        quantity:
          type: integer
          format: int64
          default: 1
          minimum: 1
          maximum: 1000000
```

This can be extended to include the `CreateOrderSchema`, `GetOrderSchema`, and `OrderItemSchema`:

```yaml
components:
...
  schemas:
...
    OrderItemSchema:
      type: object
      required:
        - product
        - size
      properties:
        product:
          type: string
        size:
          type: string
          enum:
            - small
            - medium
            - big
        quantity:
          type: integer
          format: int64
          default: 1
          minimum: 1
          maximum: 100000

    CreateOrderSchema:
      type: object
      required:
        - order
      properties:
        order:
          type: array
          minItems: 1
          items:
            $ref: "#/components/schemas/OrderItemSchema"

    GetOrderSchema:
      type: object
      required:
        - id
        - created
        - status
        - order
      properties:
        id:
          type: string
          format: uuid
        created:
          type: string
          format: date-time
        status:
          type: string
          enum:
            - created
            - paid
            - progress
            - cancelled
            - dispatched
            - delivered
        order:
          type: array
          minItems: 1
          items:
            $ref: "#/components/schemas/OrderItemSchema"
```

