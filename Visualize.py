from data_interface import CovidData
import streamlit as st
from datetime import datetime, timedelta

date = datetime.today() - timedelta(days=1)
cov_data = CovidData()
df = cov_data.get_daily_data(date)
df2 = cov_data.get_cumulative_data()

# date = st.date_input("Pick a date", value=datetime.today())
st.dataframe(df2)

