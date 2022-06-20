from data_interface import CovidData
import streamlit as st
from datetime import datetime, timedelta, date
from plotly.subplots import make_subplots
import plotly.graph_objects as go
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

states = output_df.Province_State.unique()
state = st.selectbox(
    'Please select a state from below:',
    states)
# state = "California"
with st.spinner('Loading data from source...'):
    state_df = output_df[output_df.Province_State == state]
    prev_state_df = prev_df[prev_df.Province_State == state]

    monthly_df = output_data.get_period_data(lag=60)
    state_monthly_df = monthly_df[monthly_df.Province_State == state]


#############

# Confirmed/Deaths difference with 7 days ago
diff = str(state_df['Confirmed'].iloc[0] - prev_state_df['Confirmed'].iloc[0])
death_diff = str(state_df['Deaths'].iloc[0] - prev_state_df['Deaths'].iloc[0])

# Mortality Rate
US_avg_mr_daily = output_df['Mortality_Rate'].mean(axis=0)
mort_rate_diff = str(
    round(100 * (state_df['Mortality_Rate'].iloc[0] - US_avg_mr_daily), 2)
) + "%"

# Incident Rate
US_avg_ir_daily = output_df['Incident_Rate'].mean(axis=0)
incident_rate_diff = str(
    int(state_df['Incident_Rate'].iloc[0] - US_avg_ir_daily)
)

# Average Incident Rate
US_avg_ir_monthly = monthly_df.groupby('Date').mean()['Incident_Rate']
state_monthly_df['US_Avg_Incident_Rate'] = list(US_avg_ir_monthly)
state_monthly_df['Incident_Rate'] = state_monthly_df['Incident_Rate'].astype(float)
##############

# st.dataframe(output_df)
# st.dataframe(prev_df)
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col1.metric(label='Confirmed', value=int(state_df['Confirmed'].iloc[0]),
            delta=diff,
            delta_color='inverse')
col2.metric(label='Deaths', value=int(state_df['Deaths'].iloc[0]),
            delta=death_diff,
            delta_color='inverse')
col3.metric(label='Case-Fatality Ratio (vs. US avg.)',
            value=str(round(100 * state_df['Mortality_Rate'].iloc[0], 2)) + "%",
            delta=mort_rate_diff,
            delta_color='inverse')
col4.metric(label='Incident Rate (vs. US avg.)', value=int(state_df['Incident_Rate'].iloc[0]),
            delta=incident_rate_diff,
            delta_color='inverse')

with st.container():
    fig1 = make_subplots(rows=4, cols=1,
                         subplot_titles=('Confirmed', 'Confirmed Daily Changes', 'Deaths','Deaths Daily Changes'))

    fig1.add_trace(
        go.Scatter(x=state_monthly_df['Date'],
                   y=state_monthly_df['Confirmed'],
                   line=dict(color="black")),
        row=1, col=1)

    fig1.add_trace(
        go.Scatter(x=state_monthly_df['Date'],
                   y=state_monthly_df['Confirmed'].diff(1).fillna(0),
                   line=dict(color="#FF737D")),
        row=2, col=1)

    fig1.add_trace(
        go.Scatter(x=state_monthly_df['Date'], y=state_monthly_df['Deaths'],
                   line=dict(color="black")),
        row=3, col=1)

    fig1.add_trace(
        go.Scatter(x=state_monthly_df['Date'],
                   y=state_monthly_df['Deaths'].diff(1).fillna(0),
                   line=dict(color="#FF737D")),
        row=4, col=1)

    fig1.update_layout(height=1200, width=700,
                       margin=dict(l=0, r=0, b=0, t=50, pad=4),
                       showlegend=False)
    fig1.update_xaxes(tickangle=90)
    fig1.show()
    st.plotly_chart(fig1)

    fig2 = px.line(data_frame=state_monthly_df, x='Date', y=['Incident_Rate', 'US_Avg_Incident_Rate'],
                   title="State Incident Rate vs. US Average")
    fig2.update_layout(height=400, width=700,
                       margin=dict(l=0, r=0, b=0, t=50, pad=4),
                       yaxis_title="Incident Rate:<br>cases per 100,000 persons",
                       xaxis_title=" ")
    fig2.update_xaxes(tickangle=45)
    st.plotly_chart(fig2)
