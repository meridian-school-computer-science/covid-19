# data from 22 March 2020
# https://ourworldindata.org/coronavirus-source-data
# potential state data: https://usafacts.org/visualizations/coronavirus-covid-19-spread-map/


import csv
from matplotlib import pyplot as plt
import datetime as dt
path = 'C:\\Users\\k_mac\\OneDrive\\Meridian\\h Computer Science\\Teacher Projects\\COVID\\'
filename = 'time_series_19-covid-Confirmed-25 Mar.csv'
date_title = '25 Mar'
states = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania', 'Illinois', 'Ohio', 'Georgia', 'North Carolina',
         'Michigan', 'New Jersey', 'Virginia', 'Washington', 'Arizona', 'Massachusets', 'Tennessee', 'Indiana',
         'Missouri', 'Maryland', 'Wisconsin', 'Colorado', 'Minnesota', 'South Carolina', 'Alabama', 'Louisiana', 
         'Kentucky', 'Oregon', 'Oklahoma', 'Connecticut', 'Utah', 'Puerto Rico', 'Iowa', 'Nevada', 'Arcansas',
         'Mississippi', 'Kansas', 'New Mexico', 'Nebraska', 'West Virginia', 'Idaho', 'Hawaii', 'New Hampshire',
         'Maine', 'Montana', 'Rhode Island', 'Delaware', 'South Dakota', 'North Dakota', 'Alaska', 'District of Columbia',
         'Vermont', 'Wyoming', 'Guam', 'U.S. Virgin Islands', 'American Samoa']
watch_states = ['New York', 'Washington', 'California', 'Louisiana', 'Texas', 'District of Columbia']
colors =    [ "red",        "blue",        "green",    "black",     "purple",   "orange",  "yellow" , "magenta"]

# a change also from inside github

frame = pd.read_csv(path+filename)


us_frame = frame[frame['Province/State'].isin(states)]
us_frame.set_index('Province/State', inplace=True)
us_transpose = us_frame.transpose()
us_transpose.drop(['Lat', 'Long', 'Country/Region'], inplace=True)
us_transpose.reset_index(inplace=True)
us_transpose['index'] = pd.to_datetime(us_transpose['index'], format='%m/%d/%y')

us_transpose.rename(columns = {'index': 'Date'}, inplace=True)
blank_rows = range(0, 48)
us_transpose.drop(blank_rows, inplace=True)

reference_date = pd.Timestamp.today()
# for x axis
us_transpose['Days from Today'] = us_transpose['Date'].sub(reference_date).dt.days

# set the title
plt.title('COVID-19 Confirmed Cases')
plt.title('Log Scale', loc='left')
plt.title(date_title, loc='right')


# set x current axis with a logritmetic scale that greatly helps see the pace of exponential increase
ax = plt.gca()  
plt.yscale('log')


for i, state in enumerate(watch_states): 
    us_transpose.plot(kind='line', x='Days from Today', y=state, color=colors[i], ax=ax)

plt.show()