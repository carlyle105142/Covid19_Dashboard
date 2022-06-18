from data_interface import CovidData
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px
import matplotlib.pyplot as plt


cov_data = CovidData()
df1 = cov_data.get_daily_data()

prev_cov_data = CovidData(cov_data.input_date - timedelta(days=7))
df1_prev = prev_cov_data.get_daily_data()


# df2 = cov_data.get_cumulative_data()


# fig1 = px.line(df2[df2.Province_State == 'California'], y='Confirmed')
# st.plotly_chart(fig1)
state = "California"
diff = int(df1[df1.Province_State == state]['Confirmed']) - int(df1_prev[df1_prev.Province_State == state]['Confirmed'])

st.metric(label='Confirmed', value=int(df1[df1.Province_State == state]['Confirmed']), delta=int(diff), delta_color='inverse')
