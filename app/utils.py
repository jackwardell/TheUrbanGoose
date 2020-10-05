import os
from functools import partial

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


# geocoder.reverse()
