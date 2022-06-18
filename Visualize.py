from data_interface import CovidData
import streamlit as st
from datetime import datetime, timedelta, date
import plotly.express as px
import matplotlib.pyplot as plt

d_input = st.date_input("Please choose a date", date.today() - timedelta(days=2))
dt_input = datetime(year=d_input.year, month=d_input.month, day=d_input.day)

## Output data according to user input
output_data = CovidData(desired_day=dt_input)
output_df = output_data.get_daily_data()

## 7 days prior to input date
prev_data = CovidData(output_data.input_date - timedelta(days=7))
prev_df = prev_data.get_daily_data()

## 1-month data
# monthly_df = output_data.get_period_data(lag=30)


# fig1 = px.line(df2[df2.Province_State == 'California'], y='Confirmed')
# st.plotly_chart(fig1)
state = "California"
diff = int(output_df[output_df.Province_State == state]['Confirmed']) - int(
    prev_df[prev_df.Province_State == state]['Confirmed'])
death_diff = int(output_df[output_df.Province_State == state]['Deaths']) - int(
    prev_df[prev_df.Province_State == state]['Deaths'])

# st.dataframe(output_df)
# st.dataframe(prev_df)
st.metric(label='Confirmed', value=int(output_df[output_df.Province_State == state]['Confirmed']), delta=int(diff), delta_color='inverse')
st.metric(label='Deaths', value=int(output_df[output_df.Province_State == state]['Deaths']), delta=int(death_diff), delta_color='inverse')