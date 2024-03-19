from math import radians

import bz2
import _pickle as cPickle
from sklearn.metrics.pairwise import haversine_distances
import numpy as np


def save_gherkin(data, filepath):
    """
    A compressed pickle file – a lil' pickle!
    Saves a .pbz2 files. Expect that file extension in `filepath`.
    """
    with bz2.BZ2File(filepath, "w") as write_file: 
        cPickle.dump(data, write_file)


def load_gherkin(filepath):
    """
    A compressed pickle file – a lil' pickle!
    Loads a .pbz2 files. Expect that file extension in `filepath`.
    """
    data = bz2.BZ2File(filepath, "rb")
    data = cPickle.load(data)
    return data


# def as_the_crow_flies_distance(start_lat, start_lng, end_lat, end_lng):
#     """Trigonometric distance between coordinates"""
#     try:
#         start_loc = [radians(start_lat), radians(start_lng)]
#         end_loc = [radians(end_lat), radians(end_lng)]

#         angular_distance = haversine_distances([start_loc, end_loc])

#         # multiply by Earth radius to get kilometers
#         crow_flies_distance = angular_distance[0][1] * 6371000/1000

#         # Convert to miles
#         crow_flies_distance *= 0.621371

#         return crow_flies_distance
    
#     except ValueError:
#         # Missing value
#         return np.nan





# def hex_to_rgb(hex_string):
#     hex_string = hex_string.strip("#")
#     rgb = tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))
#     return rgb