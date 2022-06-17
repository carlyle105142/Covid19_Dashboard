from data_interface import CovidData
import streamlit as st
from datetime import datetime, timedelta
import plotly.express as px
import matplotlib.pyplot as plt

date = datetime.today() - timedelta(days=1)
cov_data = CovidData()
df2 = cov_data.get_cumulative_data()


fig1 = px.line(df2[df2.Province_State == 'California'], y='Confirmed')
st.plotly_chart(fig1)
