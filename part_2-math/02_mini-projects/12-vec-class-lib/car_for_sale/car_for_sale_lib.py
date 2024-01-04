"""A class for vectors representing Cars for Sale"""
import json
from datetime import datetime
from pathlib import Path

from vec import Vector


class CarForSale(Vector):
    """A class for vectors representing Cars For Sale"""

    reference_date = datetime(2024, 1, 3, 12)

    @staticmethod
    def load_cars_from_dataset():
        def parse_date(s):
            input_format = "%m/%d - %H:%M"
            dt = datetime.strptime(s, input_format).replace(year=2018)
            return dt

        contents = (Path(__file__).parent / Path("cargraph.json")).read_text()
        objects_from_dataset = json.loads(contents)
        cleaned_objects = []

        for car in objects_from_dataset[1:]:
            try:
                clean_object = CarForSale(
                    int(car[1]),
                    float(car[3]),
                    float(car[4]),
                    parse_date(car[6]),
                    car[2],
                    car[5],
                    car[7],
                    car[8],
                )
                cleaned_objects.append(clean_object)
            except Exception:  # pylint: disable=W0718:broad-exception-caught
                pass

        return cleaned_objects

    def __init__(
        self,
        model_year,
        mileage,
        price,
        posted_datetime,
        model="(virtual)",
        source="(virtual)",
        location="(virtual)",
        description="(virtual)",
    ):
        self.model_year = model_year
        self.mileage = mileage
        self.price = price
        self.posted_datetime = posted_datetime
        self.model = model
        self.source = source
        self.location = location
        self.description = description

    @classmethod
    def zero(cls):
        return CarForSale(0, 0, 0, CarForSale.reference_date)

    def add(self, other):
        def add_dates(d1, d2):
            age1 = CarForSale.reference_date - d1
            age2 = CarForSale.reference_date - d2
            sum_age = age1 + age2
            return CarForSale.reference_date - sum_age

        if not isinstance(other, CarForSale):
            raise TypeError("Incompatible vectors")

        return CarForSale(
            self.model_year + other.model_year,
            self.mileage + other.mileage,
            self.price + other.price,
            add_dates(self.posted_datetime, other.posted_datetime),
        )

    def scale(self, scalar):
        def scale_date(d):
            age = CarForSale.reference_date - d
            return CarForSale.reference_date - (scalar * age)

        return CarForSale(
            scalar * self.model_year,
            scalar * self.mileage,
            scalar * self.price,
            scale_date(self.posted_datetime),
        )

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.model_year == other.model_year
            and self.mileage == other.mileage
            and self.price == other.price
            and self.posted_datetime == other.posted_datetime
            and self.model == other.model
            and self.source == other.source
            and self.location == other.location
            and self.description == other.description
        )

    def __str__(self):
        """User friendly representation for users of the code"""
        return (
            f"(model_year={self.model_year}, "
            f"mileage={self.mileage}, "
            f"price={self.price}, "
            f"posted_datetime={self.posted_datetime}, "
            f"model={self.model}, "
            f"source={self.source}, "
            f"location={self.location}, "
            f"description={self.description})"
        )

    def __repr__(self):
        """Dev oriented representation for debugging purposes"""
        return (
            f"CarForSale(model_year={self.model_year}, "
            f"mileage={self.mileage}, "
            f"price={self.price}, "
            f"posted_datetime={self.posted_datetime}, "
            f"model={self.model}, "
            f"source={self.source}, "
            f"location={self.location}, "
            f"description={self.description})"
        )
