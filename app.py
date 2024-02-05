import streamlit as st

from src import rides
from src import logic as lg


df = rides.load_data()
st.write(df)
lg.map_start_and_end_locations(df)