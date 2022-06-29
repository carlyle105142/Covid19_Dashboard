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

st.title('COVID-19 Dashboard')

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

##################
# Key Metrices per state#
##################


# Confirmed/Deaths difference with 7 days ago
confirmed_diff = str(state_df['Confirmed'].iloc[0] - prev_state_df['Confirmed'].iloc[0])
death_diff = str(state_df['Deaths'].iloc[0] - prev_state_df['Deaths'].iloc[0])

# Confirmed/Deaths 7-Day MA
confirmed_ma = state_monthly_df['Confirmed'].rolling(7).mean()
death_ma = state_monthly_df['Deaths'].rolling(7).mean()

confirmed_ma.fillna(confirmed_ma.iloc[6], inplace=True)
death_ma.fillna(death_ma.iloc[6], inplace=True)

# Confirmed/Deaths 7-Day delta MA
confirmed_delta_ma = state_monthly_df['Confirmed'].diff(1).rolling(7).mean()
death_delta_ma = state_monthly_df['Deaths'].diff(1).rolling(7).mean()

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

##################
##All State Data##
##################

all_states_df = output_df.drop(columns=['Lat', 'Long_'])

# Goals:
# Identify 7-day moving average curve (Confirmed and Deaths)
# Find out if recent increases are worth alert
# Write out the key questions of interest
# Give a pie chart of total number of confirmed cases
# Give a ranking of incident rate among all states (daily)


#################
##Visualization##
#################
date_str = output_data.date_str
st.subheader('Latest Update ({0})'.format(date_str))

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)
col1.metric(label='Confirmed (vs. Last Week)', value=int(state_df['Confirmed'].iloc[0]),
            delta=confirmed_diff,
            delta_color='inverse')
col2.metric(label='Deaths (vs. Last Week)', value=int(state_df['Deaths'].iloc[0]),
            delta=death_diff,
            delta_color='inverse')
col3.metric(label='Case-Fatality Ratio (vs. US Avg.)',
            value=str(round(100 * state_df['Mortality_Rate'].iloc[0], 2)) + "%",
            delta=mort_rate_diff,
            delta_color='inverse')
col4.metric(label='Incident Rate (vs. US avg.)', value=int(state_df['Incident_Rate'].iloc[0]),
            delta=incident_rate_diff,
            delta_color='inverse')
st.header('   ')
option = st.selectbox(
    'Which plot would you like to look at?',
    ('Confirmed Cases', 'Deaths', 'Incident Rate'))
if option == "Confirmed Cases":
    with st.container():
        st.subheader('Confirmed Cases')
        fig1 = make_subplots(rows=1, cols=1,
                             specs=[[{"secondary_y": True}]])

        fig1.add_trace(
            go.Scatter(x=state_monthly_df['Date'],
                       y=state_monthly_df['Confirmed'],
                       line=dict(color="black", shape='spline'), name='Confirmed', legendgroup='1'),
            row=1, col=1,
            secondary_y=False)
        # state_monthly_df['Confirmed'].diff(1).fillna(0)
        fig1.add_trace(
            go.Scatter(x=state_monthly_df['Date'],
                       y=confirmed_delta_ma,
                       line=dict(color="#FF737D", shape='spline'), opacity=0.5, name='Rate of Change', legendgroup='1'),
            row=1, col=1,
            secondary_y=True)
        fig1.update_yaxes(title_text="Number of Confirmed Cases", secondary_y=False)
        fig1.update_yaxes(title_text="Daily Changes", secondary_y=True)

        fig1.update_layout(height=400, width=700,
                           margin=dict(l=70, r=10, b=30, t=30, pad=4))
        st.plotly_chart(fig1)
if option == "Deaths":
    with st.container():
        st.subheader('Deaths')
        fig2 = make_subplots(rows=1, cols=1,
                             specs=[[{"secondary_y": True}]])
        fig2.add_trace(
            go.Scatter(x=state_monthly_df['Date'],
                       y=state_monthly_df['Deaths'],
                       line=dict(color="black", shape='spline'), name='Deaths', legendgroup='2'),
            row=1, col=1,
            secondary_y=False)
        # state_monthly_df['Deaths'].diff(1).fillna(0)
        fig2.add_trace(
            go.Scatter(x=state_monthly_df['Date'],
                       y=death_delta_ma,
                       line=dict(color="#9999FF", shape='spline'), name='Rate of Change', opacity=0.5, legendgroup='2'),
            row=1, col=1,
            secondary_y=True)

        fig2.update_yaxes(title_text="Number of Deaths", secondary_y=False)
        fig2.update_yaxes(title_text="Daily Changes", secondary_y=True)

        fig2.update_layout(height=400, width=700,
                           margin=dict(l=70, r=10, b=30, t=30, pad=4))
        st.plotly_chart(fig2)
if option == "Incident Rate":
    temp = list(states)
    temp.remove(state)
    temp.insert(0, "US Average")
    compared_state = st.selectbox('Which state to compare with?', temp)

    if compared_state == "US Average":
        with st.container():
            st.subheader('State Incident Rate vs. US Average')
            fig3 = px.line(data_frame=state_monthly_df, x='Date', y=['Incident_Rate', 'US_Avg_Incident_Rate'])
            fig3.update_layout(height=400, width=700,
                               margin=dict(l=0, r=0, b=30, t=30, pad=4),
                               yaxis_title="Incident Rate:<br>cases per 100,000 persons",
                               xaxis_title=" ",
                               legend_title=" ")
            new_names = {'Incident_Rate': 'State Incident Rate', 'US_Avg_Incident_Rate': 'US Average Incident Rate'}
            fig3.for_each_trace(lambda t: t.update(name=new_names[t.name],
                                                   legendgroup=new_names[t.name],
                                                   hovertemplate=t.hovertemplate.replace(t.name, new_names[t.name])
                                                   )
                                )
            st.plotly_chart(fig3)
    else:
        with st.container():
            st.subheader('Incident Rate: {0} vs. {1}'.format(state, compared_state))

            compared_state_monthly_df = monthly_df[monthly_df.Province_State == compared_state]

            fig3 = make_subplots(rows=1, cols=1)
            fig3.add_trace(
                go.Scatter(x=state_monthly_df['Date'],
                           y=state_monthly_df['Incident_Rate'],
                           line=dict(color="black", shape='spline'), name=state),
                row=1, col=1)
            fig3.add_trace(
                go.Scatter(x=compared_state_monthly_df['Date'],
                           y=compared_state_monthly_df['Incident_Rate'],
                           line=dict(color="red", shape='spline'), name=compared_state),
                row=1, col=1)
            fig3.update_layout(height=400, width=700,
                               margin=dict(l=0, r=0, b=30, t=30, pad=4),
                               yaxis_title="Incident Rate:<br>cases per 100,000 persons",
                               xaxis_title=" ",
                               legend_title=" ")
            st.plotly_chart(fig3)
