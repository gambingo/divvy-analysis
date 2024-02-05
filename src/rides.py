import pandas as pd

from .directories import DATA_DIR
from src import utils


def load_data():
    filename = "202307-divvy-tripdata.csv"
    df = pd.read_csv(DATA_DIR / filename)
    df = clean_and_transform_data(df)
    return df


def clean_and_transform_data(df):
    # Timestamp Columns
    _format = "%Y-%m-%d %H:%M:%S"
    timestamp_columns = ["started_at", "ended_at"]
    for col in timestamp_columns:
        df[col] = pd.to_datetime(df[col], format=_format)

    # Duration
    ## Some rides are reported as taking multiple days. While others take
    ## -3 seconds. The short, time-traveling ones are likely false starts. 
    ## Unsure what's going on with the crazy longs. Regardless, let's remove
    ## the unrealistic trips.
    df["duration"] = df["ended_at"] - df["started_at"]

    ## Exclude greater than 1 day
    too_long = df["duration"].apply(lambda td: td.days > 0)
    df = df[~too_long]

    ## Exclude greater than 8 hours
    too_long = df["duration"].apply(lambda td: td.seconds/60/60 > 8)
    df = df[~too_long]

    ## Exclude less than 10 seconds
    too_short = df["duration"].apply(lambda td: td.seconds < 10)
    df = df[~too_short]

    # Distance
    ## Remove rows with missing location data. We can't use them.
    missing = df[["start_lat", "start_lng", "end_lat", "end_lng"]].isnull()
    df = df[~missing.any(axis=1)]

    ## distance (in miles)
    # crow_flies = lambda row: utils.as_the_crow_flies_distance(row.start_lat, 
    #                                                     row.start_lng, 
    #                                                     row.end_lat, 
    #                                                     row.end_lng)
    # df["distance"] = df.apply(crow_flies, axis=1)

    return df