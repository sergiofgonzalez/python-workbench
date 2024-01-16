"""In-memory representation of the application data"""
from datetime import datetime

ingredients = [
    {
        "id": "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d",
        "name": "Milk",
        "stock": {"quantity": 100.0, "unit": "LITERS"},
        "products": [],
        "lastUpdated": datetime.utcnow(),
    }
]


products = [
    {
        "id": "910095bf-980b-455e-8d47-48394b6deba0",
        "name": "Walnut Bomb",
        "price": 37.0,
        "available": False,
        "ingredients": [
            {
                "ingredient": "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d",
                "quantity": 100.0,
                "unit": "LITERS",
            },
        ],
        "hasFilling": False,
        "hasNutsOnTopOption": True,
        "lastUpdated": datetime.utcnow(),
    },
    {
        "id": "c8d5c681-6c44-4c9e-bf94-5a238ec93e37",
        "name": "Capuccino Star",
        "price": 12.50,
        "size": "SMALL",
        "available": True,
        "ingredients": [
            {
                "ingredient": "cb0db1b5-e03d-45b5-961c-bfd5a4c7629d",
                "quantity": 75.55,
                "unit": "LITERS",
            },
        ],
        "hasCreamOnTopOption": True,
        "hasServeOnIceOption": True,
        "lastUpdated": datetime.utcnow(),
    },
]
