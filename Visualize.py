from data_interface import CovidData
import streamlit as st
from datetime import datetime

cov_data = CovidData()

df = cov_data.cumulative_df

col_names = ['Province_State', 'Confirmed', 'Deaths', 'Recovered', 'Active',
             'Incident_Rate', 'Testing_Rate', 'Hospitalization_Rate', 'Mortality_Rate']

st.dataframe(df)
