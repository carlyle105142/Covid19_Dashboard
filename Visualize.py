from data_interface import CovidData
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px

date = datetime.today() - timedelta(days=1)
cov_data = CovidData()
# df = cov_data.get_daily_data(date)
df2 = cov_data.get_cumulative_data()

# date = st.date_input("Pick a date", value=datetime.today())
fig1 = px.line(df2[df2.Province_State == 'California'], x='date', y='Confirmed')
st.plotly_chart(fig1, use_container_width=True)
# st.line_chart(df2[df2.Province_State == 'California']['Confirmed'].diff())
# st.line_chart(df2[df2.Province_State == 'California']['Deaths'].diff())
# states = df2.index.unique()

