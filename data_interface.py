import pandas as pd
from datetime import datetime, timedelta


class CovidData:
    def __init__(self, desired_day=datetime.today()-timedelta(days=2)):
        self.start_date = datetime(year=2020, month=4, day=12)
        self.input_date = desired_day
        if self.input_date < self.start_date:
            raise ValueError('Please choose a date after 2020/04/12!')
        self.date_str = self.input_date.strftime('%m-%d-%Y')
        self.col_name = ['Province_State', 'Confirmed', 'Deaths',
                         'Recovered','Incident_Rate', 'Lat', 'Long_']

    @staticmethod
    def make_url(desired_day):
        url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
              '/csse_covid_19_daily_reports_us/'
        return url + desired_day.strftime('%m-%d-%Y') + '.csv'

    def get_daily_data(self, desired_day=None):
        if desired_day is None:
            desired_day = self.input_date
        url = self.make_url(desired_day)
        daily_df0 = pd.read_csv(url)  # get the daily data .csv file from source url

        daily_df = daily_df0[daily_df0['ISO3'] == 'USA'][self.col_name]
        daily_df['Date'] = desired_day.strftime('%m-%d-%Y')
        # daily_df.set_index('Date', inplace=True)

        daily_df.dropna(subset=['Lat', 'Long_'], inplace=True)
        daily_df[['Confirmed', 'Deaths']] = daily_df[['Confirmed', 'Deaths']].astype(int)
        daily_df['Mortality_Rate'] = daily_df['Deaths'] / daily_df['Confirmed']

        return daily_df

    def get_period_data(self, lag=30):

        def date_range(start_date, end_date):
            for n in range(int((end_date - start_date).days)):
                yield start_date + timedelta(n)

        start = self.input_date - timedelta(days=lag)
        end = self.input_date

        col_name = self.get_daily_data(start).columns
        final_df = pd.DataFrame(columns=col_name)

        for date in date_range(start, end):
            sub_df = self.get_daily_data(date)
            final_df = pd.concat([final_df, sub_df])

        return final_df

# a = CovidData()
# print(a.daily_df)
