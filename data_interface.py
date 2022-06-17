import pandas as pd
from datetime import datetime, timedelta
import os.path
import streamlit as st


st.cache()


class CovidData:
    def __init__(self, desired_day=datetime.today(), get_cumulative_data=False):
        self.start_date = datetime(year=2020, month=4, day=12)
        self.input_date = desired_day
        if self.input_date < self.start_date:
            raise ValueError('Please choose a date after 2020/04/12!')
        self.date_str = self.input_date.strftime('%m-%d-%Y')
        self.daily_df = self.get_daily_data(desired_day - timedelta(days=1))

        if get_cumulative_data is True:
            self.is_cumulative_obtained = False
            self.local_file_exists = os.path.exists('up_to_{0}.csv'.format(self.date_str))
            if self.local_file_exists is False:
                self.cumulative_df = self.get_cumulative_data()
                self.cumulative_df.to_csv('up_to_{0}.csv'.format(self.date_str), index=False)
            else:
                self.cumulative_df = pd.read_csv('up_to_{0}.csv'.format(self.date_str))

    @staticmethod
    def make_url(desired_day):
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
              '/csse_covid_19_daily_reports_us/'
        return url + desired_day.strftime('%m-%d-%Y') + '.csv'

    def get_daily_data(self, desired_day):

        url = self.make_url(desired_day)
        daily_df0 = pd.read_csv(url)  # get the daily data .csv file from source url
        col_name = ['Province_State', 'Confirmed', 'Deaths', 'Recovered', 'Active',
                    'Incident_Rate', 'Testing_Rate', 'Hospitalization_Rate', 'Lat', 'Long_']

        daily_df = daily_df0[daily_df0['ISO3'] == 'USA'][col_name]
        daily_df['date'] = desired_day.strftime('%m-%d-%Y')
        daily_df.set_index('Province_State', inplace=True)

        daily_df.dropna(subset=['Lat', 'Long_'], inplace=True)
        # daily_df.drop(columns='Lat', inplace=True)
        daily_df[['Confirmed', 'Deaths']] = daily_df[['Confirmed', 'Deaths']].astype(float)
        daily_df['Mortality_Rate'] = daily_df['Deaths'] / daily_df['Confirmed']

        return daily_df

        # define a function to loop over given date range

    def get_cumulative_data(self):

        def date_range(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        if self.is_cumulative_obtained is True:
            print('Cumulative data already obtained!')
        else:
            final_df = pd.DataFrame(
                columns=['Province_State', 'Confirmed', 'Deaths', 'Recovered', 'Active',
                         'Incident_Rate', 'Testing_Rate', 'Hospitalization_Rate', 'Mortality_Rate', 'Lat', 'Long_'])
            start = self.start_date
            end = self.input_date

            if start == end:
                return self.get_daily_data(start)
            else:
                for date in date_range(start, end):
                    sub_df = self.get_daily_data(date)
                    final_df = pd.concat([final_df, sub_df])

            # update df and status
            self.is_cumulative_obtained = True
            return final_df


# a = CovidData()
# print(a.daily_df)

