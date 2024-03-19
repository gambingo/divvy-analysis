from math import radians

import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.metrics.pairwise import haversine_distances



def clean_and_transform_data(df):
    # Timestamp Columns
    _format = "%Y-%m-%d %H:%M:%S"
    timestamp_columns = ["started_at", "ended_at"]
    for col in timestamp_columns:
        df[col] = pd.to_datetime(df[col], format=_format)

    # Duration
    df["duration"] = df["ended_at"] - df["started_at"]
    timedelta_to_seconds = lambda td: td.days*24*60*60 + td.seconds
    df["duration_seconds"] = df["duration"].apply(timedelta_to_seconds)

    # Distance
    ## Remove rows with missing location data. We can't use them.
    missing = df[["start_lat", "start_lng", "end_lat", "end_lng"]].isnull()
    df = df[~missing.any(axis=1)]

    ## Straight Line Distance
    ## This is computationally a little much, so we do it ahead of time.
    tqdm.pandas(desc="Calculating As-The-Crow-Flies Distance")
    df["straight_line_distance_miles"] = df.progress_apply(
        lambda row: as_the_crow_flies_distance(row.start_lat, row.start_lng, row.end_lat, row.end_lng),
        axis=1
    )

    # Same Start and End Location
    ## This will be a derived feature, that may change, since we can
    ## incorporate station-less trips that end too close together
    # df["same_start_and_end"] = df["start_station_id"] == df["end_station_id"]

    df = enfore_data_types(df)
    return df


def enfore_data_types(df):
    # This list includes only columns whos data types we will need to coerce
    data_types = {
        "start_station_id":     str,
        "end_station_id":       str,
    }

    for col, dtype in data_types.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)
            
    return df




# def calculate_distance(df):
#     """After filtering, calculate the straight-line distance of the trip"""
#     # distance (in miles)
#     crow_flies = lambda row: as_the_crow_flies_distance(row.start_lat,
#                                                               row.start_lng,
#                                                               row.end_lat,
#                                                               row.end_lng)
#     df["distance"] = df.apply(crow_flies, axis=1)
#     return df


def as_the_crow_flies_distance(start_lat, start_lng, end_lat, end_lng):
    """Trigonometric distance between coordinates"""
    try:
        start_loc = [radians(start_lat), radians(start_lng)]
        end_loc = [radians(end_lat), radians(end_lng)]

        angular_distance = haversine_distances([start_loc, end_loc])

        # multiply by Earth radius to get kilometers
        crow_flies_distance = angular_distance[0][1] * 6371000/1000

        # Convert to miles
        crow_flies_distance *= 0.621371

        return crow_flies_distance
    
    except ValueError:
        # Missing value
        return np.nan