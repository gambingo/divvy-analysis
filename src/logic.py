import pandas as pd
import streamlit as st

from src import utils


def map_start_and_end_locations(df):
    """
    transforms the ride history dataframe so it's a valid. color-coded input 
    for st.map
    """
    # green = "#5C8516"
    # burnt = "#AE4600"
    # green = utils.hex_to_rgb(green)
    # burnt = utils.hex_to_rgb(burnt)

    starts = df[["start_lat", "start_lng"]]
    # starts["color"] = [green]*starts.shape[0]
    starts = starts.rename(columns={"start_lat": "lat", "start_lng": "lon"})

    ends = df[["end_lat", "end_lng"]]
    # ends["color"] = [burnt]*ends.shape[0]
    ends = ends.rename(columns={"end_lat": "lat", "end_lng": "lon"})

    chart_df = pd.concat([starts, ends]).dropna()
    st.write(chart_df)
    st.write(chart_df["color"].iloc[0])
    st.map(chart_df)