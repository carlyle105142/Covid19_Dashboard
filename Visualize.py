from data_interface import CovidData
import streamlit as st
from datetime import datetime


cov_data = CovidData(datetime(2021,8,21))
df = cov_data.daily_df

st.dataframe(df)
