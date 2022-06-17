from data_interface import CovidData
import streamlit as st
from datetime import datetime


cov_data = CovidData()
df = cov_data.daily_df

date = st.date_input("Pick a date", value=datetime.today())
