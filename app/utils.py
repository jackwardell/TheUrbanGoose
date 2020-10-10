import os
from functools import partial

from app.static import FoodOrDrink
from mapbox import Geocoder

MAPBOX_API_ACCESS_TOKEN = os.getenv("MAPBOX_API_ACCESS_TOKEN")

geocoder = Geocoder(access_token=MAPBOX_API_ACCESS_TOKEN)

location_types = ["address", "poi"]

forward = partial(
    geocoder.forward,
    types=location_types,
    # limit=10,
    # country=["GB"],
    # languages="en",
    bbox=[-0.489, 51.28, 0.236, 51.686],
)


# @attr.s
# class Location:
#     restaurant = attr.ib()
#     address = attr.ib()
#     latitude = attr.ib()
#     longitude = attr.ib()
#
#     @classmethod
#     def from_query(cls, query):
#         params = {
#             "restaurant": query["restaurant"],
#             "address": query["address"],
#             "latitude": query["latitude"],
#             "longitude": query["longitude"],
#         }
#         return cls(**params)


def search_location(location, limit=10):
    query = forward(location, limit=limit)
    results = query.json()["features"]
    rv = [
        {
            "address": i["place_name"],
            "name": i["text"],
            "latitude": i["geometry"]["coordinates"][0],
            "longitude": i["geometry"]["coordinates"][1],
        }
        for i in results
    ]

    return rv


def request_to_record(request) -> bool:
    return (
        url_to_record(request.path)
        if request.remote_addr != "127.0.0.1"
        else False
    )


def url_to_record(path: str) -> bool:
    """
    >>> url_to_record("/static/hello.css")
    False
    >>> url_to_record("/api/location")
    False
    >>> url_to_record("/_debug_toolbar/")
    False
    >>> url_to_record("/admin/dashboard")
    True
    """
    return not any(["/static/" in path, "/api/" in path, "/_" in path])


def get_food_and_or_drink(*, for_drink: bool, for_food: bool) -> str:
    if for_food is True and for_drink is True:
        return FoodOrDrink.BOTH
    if for_food is True and for_drink is False:
        return FoodOrDrink.FOOD
    if for_food is False and for_drink is True:
        return FoodOrDrink.DRINK
    # if for_food is True or for_drink is True:
    #     return FoodOrDrink.EITHER
    else:
        raise ValueError("Cannot be neither food nor drink")
