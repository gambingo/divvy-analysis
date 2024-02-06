import os
import pandas as pd

from .directories import DATA_DIR
from src import utils


def load_data(recalculate=False):
    filepath = DATA_DIR / "july_rides_cleaned.pzb2"

    if recalculate or not os.path.exists(filepath):
        filename = "202307-divvy-tripdata.csv"
        df = pd.read_csv(DATA_DIR / filename)
        df = clean_and_transform_data(df)
        df = reduce_data(df)
        df = calculate_distance(df)
        utils.save_gherkin(df, filepath)
    
    else:
        df = utils.load_gherkin(filepath)

    return df


def clean_and_transform_data(df):
    # Timestamp Columns
    _format = "%Y-%m-%d %H:%M:%S"
    timestamp_columns = ["started_at", "ended_at"]
    for col in timestamp_columns:
        df[col] = pd.to_datetime(df[col], format=_format)

    # Same Start and End Location
    df["same_start_and_end"] = df["start_station_id"] == df["end_station_id"]

    # Duration
    df["duration"] = df["ended_at"] - df["started_at"]
    timedelta_to_seconds = lambda td: td.days*24*60*60 + td.seconds
    df["seconds"] = df["duration"].apply(timedelta_to_seconds)

    # Distance
    ## Remove rows with missing location data. We can't use them.
    missing = df[["start_lat", "start_lng", "end_lat", "end_lng"]].isnull()
    df = df[~missing.any(axis=1)]
    return df


def reduce_data(df):
    """
    Based on our derived features, filter down data to just what we want to
    analyze
    """
    # Remove Round Trips
    ## To plot paths, we need to remove the trips that start and end at the 
    ## same station
    df = df[~df["same_start_and_end"]]

    # Duration
    ## Some rides are reported as taking multiple days. While others take
    ## -3 seconds. The short, time-traveling ones are likely false starts. 
    ## Unsure what's going on with the crazy longs. Regardless, let's remove
    ## the unrealistic trips.
    ## Exclude greater than 1 day
    too_long = df["duration"].apply(lambda td: td.days > 0)
    df = df[~too_long]

    ## Exclude greater than 2 hours
    ## Early EDA showed that 99.5% of rides were less than 123 minutes.
    too_long = df["duration"].apply(lambda td: td.seconds/60/60 > 8)
    df = df[~too_long]

    ## Exclude less than 10 seconds
    too_short = df["duration"].apply(lambda td: td.seconds < 10)
    df = df[~too_short]

    return df


def calculate_distance(df):
    """After filtering, calculate the straight-line distance of the trip"""
    # distance (in miles)
    crow_flies = lambda row: utils.as_the_crow_flies_distance(row.start_lat,
                                                              row.start_lng,
                                                              row.end_lat,
                                                              row.end_lng)
    df["distance"] = df.apply(crow_flies, axis=1)
    return df