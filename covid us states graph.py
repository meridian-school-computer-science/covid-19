import pandas as pd
import csv
from matplotlib import pyplot as plt
import datetime as dt

# https://www.worldometers.info/coronavirus/

# https://www.statista.com/topics/6084/coronavirus-covid-19-in-the-us/



# here is a new line



path = 'C:\\Users\\k_mac\\OneDrive\\Meridian\\h Computer Science\\Teacher Projects\\COVID\\data\\us\\'
filename = 'mac_us_states_deaths.csv'
date_title = '15 Sep'
death_rate_adjustment = 250

states = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania', 'Illinois', 'Ohio', 'Georgia', 'North Carolina',
         'Michigan', 'New Jersey', 'Virginia', 'Washington', 'Arizona', 'Massachusetts', 'Tennessee', 'Indiana',
         'Missouri', 'Maryland', 'Wisconsin', 'Colorado', 'Minnesota', 'South Carolina', 'Alabama', 'Louisiana', 
         'Kentucky', 'Oregon', 'Oklahoma', 'Connecticut', 'Utah', 'Puerto Rico', 'Iowa', 'Nevada', 'Arcansas',
         'Mississippi', 'Kansas', 'New Mexico', 'Nebraska', 'West Virginia', 'Idaho', 'Hawaii', 'New Hampshire',
         'Maine', 'Montana', 'Rhode Island', 'Delaware', 'South Dakota', 'North Dakota', 'Alaska', 'District of Columbia',
         'Vermont', 'Wyoming', 'Guam', 'U.S. Virgin Islands', 'American Samoa']

state_abbreviation = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                       'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                       'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                       'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                       'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC']

frame = pd.read_csv(path+filename)


states_of_interest = ['NY', 'CA NY+1', 'LA NY+3', 'NJ NY+4', 'MI NY+7', 'TX NY+9', 'PA NY+9']  
# holding  , 'FL NY+14',   'WA NY+14'
colors =            [ "red",        "blue",   "green",  "purple",    "black",   "orange",        "yellow" , "magenta"]
                     
frame = pd.read_csv(path+filename)
frame.set_index('State', inplace=True)

us_transpose = frame.transpose()
us_transpose.reset_index(inplace=True)

us_transpose.rename(columns = {'index': 'Date'}, inplace=True)
us_transpose['Date'] = pd.to_datetime(us_transpose['Date'])
# , format='%m/%d/%y'
# reference date
reference_date = pd.Timestamp.today()
# for x axis
us_transpose['Days from Today'] = us_transpose['Date'].sub(reference_date).dt.days

# build date adjustment State data
us_transpose['NY'] = death_rate_adjustment * us_transpose['New York']
us_transpose['LA NY+3'] = death_rate_adjustment * us_transpose['Louisiana'].shift(periods=-3)
us_transpose['CA NY+1'] = death_rate_adjustment * us_transpose['California'].shift(periods=-1)
us_transpose['NJ NY+4'] = death_rate_adjustment * us_transpose['New Jersey'].shift(periods=-4)
#us_transpose['WA NY+14'] = death_rate_adjustment * us_transpose['Washington'].shift(periods=-14)
#us_transpose['FL NY+14'] = death_rate_adjustment * us_transpose['Florida'].shift(periods=-14)
us_transpose['TX NY+9'] = death_rate_adjustment * us_transpose['Texas'].shift(periods=-9)
us_transpose['MI NY+7'] = death_rate_adjustment * us_transpose['Michigan'].shift(periods=-7)
us_transpose['PA NY+9'] = death_rate_adjustment * us_transpose['Pennsylvania'].shift(periods=-9)

fig=plt.figure(figsize=(10,8))
# set the title
plt.title('States COVID-19 Estimated Cases')
plt.title('Log Scale', loc='left')
plt.title(date_title, loc='right')
#plt.title('Linear', loc='left')

ax = plt.gca()  # get current axis
plt.yscale('log')
#plt.yscale('linear')
for i, state in enumerate(states_of_interest): 
    us_transpose.plot(kind='line', x='Days from Today', y=state, color=colors[i], ax=ax)

plt.show()