from data_interface import CovidData
import streamlit as st
from datetime import datetime, timedelta, date
import plotly.express as px
import matplotlib.pyplot as plt

# d_input = st.date_input("Please choose a date", date.today() - timedelta(days=2))
# dt_input = datetime(year=d_input.year, month=d_input.month, day=d_input.day)

## Output data according to user input
output_data = CovidData()
output_df = output_data.get_daily_data()

## 7 days prior to input date
prev_data = CovidData(output_data.input_date - timedelta(days=7))
prev_df = prev_data.get_daily_data()

## 1-month data
# monthly_df = output_data.get_period_data(lag=30)



# state = "California"
state = st.selectbox(
     'Please select a state from below:',
     output_df.Province_State.unique())

state_df = output_df[output_df.Province_State == state]
prev_state_df = prev_df[prev_df.Province_State == state]

monthly_df = output_data.get_period_data(lag=30)
state_monthly_df = monthly_df[monthly_df.Province_State == state]

diff = str(state_df['Confirmed'][0] - prev_state_df['Confirmed'][0])
death_diff = str(state_df['Deaths'][0] - prev_state_df['Deaths'][0])

US_avg_mort = output_df['Mortality_Rate'].mean(axis=0)
mort_rate_diff = str(
    round(100*(state_df['Mortality_Rate'][0] - US_avg_mort), 2)
)+"%"

US_avg_incident = output_df['Incident_Rate'].mean(axis=0)
incident_rate_diff = str(
    int(state_df['Incident_Rate'][0] - US_avg_incident)
)

# st.dataframe(output_df)
# st.dataframe(prev_df)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col1.metric(label='Confirmed', value=int(state_df['Confirmed'][0]),
            delta=diff,
            delta_color='inverse')
col2.metric(label='Deaths', value=int(state_df['Deaths'][0]),
            delta=death_diff,
            delta_color='inverse')
col3.metric(label='Case-Fatality Ratio \n(vs. US avg.)',
            value=str(round(100*state_df['Mortality_Rate'][0], 2))+"%",
            delta=mort_rate_diff,
            delta_color='inverse')
col4.metric(label='Incident Rate \n(vs. US avg.)', value=int(state_df['Incident_Rate'][0]),
            delta=incident_rate_diff,
            delta_color='inverse')

fig1 = px.line(state_monthly_df, y='Confirmed')
st.plotly_chart(fig1)

fig2 = px.line(state_monthly_df, y='Deaths', color='red')
st.plotly_chart(fig2)
