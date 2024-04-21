import googlemaps
from dotenv import  load_dotenv

import os
import json

load_dotenv()

API_KEY = os.getenv('GCP_API_KEY')

gmaps = googlemaps.Client(key=API_KEY)

coords = [
    (41.11801808551439, -85.10837226249447), # Walb Student Union
    (41.127906906491546, -85.09622787719132),# St. Joe Place
    (41.12416006337346, -85.10480245879863), # Canterbury Green Apartments
    (41.13138075332045, -85.14198490112749), # Regal ColdWater Crossing
    (41.07307497581807, -85.19890961647158), # AMC CLASSIC Jefferson Point 18
    (41.11180131117978, -85.1441343152665),  # Burlington
]

response = gmaps.distance_matrix(coords, coords)
print(json.dumps(response))


