import pandas as pd
from datetime import datetime, timedelta



class CovidData:
    def __init__(self, desired_day=datetime.today() - timedelta(days=3)):
        self.start_date = datetime(year=2020, month=4, day=12)
        self.dt = desired_day
        if self.dt < self.start_date:
            raise ValueError
        self.date_str = self.dt.strftime('%m-%d-%Y')

        self.is_cumulative_obtained = False
        self.url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/'
        self.df = self.get_cumulative_data()

    def make_url(self, desired_day):
        return self.url + desired_day.strftime('%m-%d-%Y') + '.csv'

    def get_daily_data(self, desired_day):

        url = self.make_url(desired_day)
        daily_df0 = pd.read_csv(url)  # get the daily data .csv file from source url
        col_name = ['Province_State', 'Confirmed', 'Deaths', 'Recovered', 'Active',
                    'Incident_Rate', 'Testing_Rate', 'Hospitalization_Rate', 'Lat']

        daily_df = daily_df0[daily_df0['ISO3'] == 'USA'][col_name]
        daily_df['date'] = desired_day.strftime('%m-%d-%Y')
        daily_df.set_index('date', inplace=True)

        daily_df.dropna(subset=['Lat'], inplace=True)
        daily_df.drop(columns='Lat', inplace=True)
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
                         'Incident_Rate', 'Testing_Rate', 'Hospitalization_Rate', 'Mortality_Rate'])
            start = self.start_date
            end = self.dt

            if start == end:
                return self.get_daily_data(start)

            else:
                for date in date_range(start, end):
                    sub_df = self.get_daily_data(date)
                    final_df = pd.concat([final_df, sub_df])

            # update df and status
            self.is_cumulative_obtained = True
            return final_df


a = CovidData()
df = a.df
