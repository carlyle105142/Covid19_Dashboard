from data_interface import CovidData
import streamlit as st
from datetime import datetime

cov_data = CovidData()

df = cov_data.daily_df

st.dataframe(df)
