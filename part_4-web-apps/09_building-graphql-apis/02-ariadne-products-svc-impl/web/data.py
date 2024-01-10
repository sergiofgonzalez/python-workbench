"""In-memory representation of the application data"""
from datetime import datetime

ingredients = [
    {
        "id": "17fc61c1-7517-4ac9-8c30-d7c7e4c90944",
        "name": "Milk",
        "stock": {"quantity": 100.0, "unit": "LITERS"},
        "products": [],
        "lastUpdated": datetime.utcnow(),
    }
]
