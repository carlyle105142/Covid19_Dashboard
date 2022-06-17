from API import CovidData
import streamlit as st
from datetime import datetime

cov_data = CovidData(desired_day=datetime(2020,9,11))
df = cov_data.df

col_names = ['Province_State', 'Confirmed', 'Deaths', 'Recovered', 'Active',
             'Incident_Rate', 'Testing_Rate', 'Hospitalization_Rate', 'Mortality_Rate']

st.table(df.head(3))
