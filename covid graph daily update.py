# data from 22 March 2020
# https://ourworldindata.org/coronavirus-source-data
# potential state data: https://data.world/covid-19-data-resource-hub/covid-19-case-counts/workspace/file?filename=COVID-19+Cases.csv

import pandas as pd
import csv
from matplotlib import pyplot as plt
import datetime as dt
path = 'C:\\Users\\k_mac\\OneDrive\\Meridian\\h Computer Science\\Teacher Projects\\COVID\\'
filename = 'total_cases_25_mar.csv'
date_title = '25 Mar'

# a change also from inside github

frame = pd.read_csv(path+filename)
frame['date'] = pd.to_datetime(frame.date, format='%Y-%m-%d')

# Which Countries are we going to graph
countries = ['Italy', 'France Italy+8', 'Germany Italy+8', 'USA Italy+12', 'Denmark Italy+14', 'UK Italy+13', 'Japan', 'Spain Italy+8' ]
colors =    [ "red",  "blue",           "green",           "black",        "purple",           "orange",  "magenta",   'yellow']
reference_date = pd.Timestamp.today()

frame3 = pd.DataFrame(frame, columns=['date', 'Italy', 'France', 'Germany', 'United States of America', 'Denmark', 'Japan', 'United Kingdom', 'Spain'])

# for x axis
frame3['Days from Today'] = frame3['date'].sub(reference_date).dt.days

# manually adjust a Country's graph based on Italy
# these lines shift their data column so it will align with Italy graph at the point that their outbreak became a problem
# 
# looking for points where a country's graph drops off of Italy's line (note: Japan from the start, and Denmark)
# limitation on this graph is data based on each nation's testing (that varies)

frame3['France Italy+8'] = frame3['France'].shift(periods=-8)
frame3['Germany Italy+8'] = frame3['Germany'].shift(periods=-8)
frame3['Denmark Italy+14'] = frame3['Denmark'].shift(periods=-14)
frame3['USA Italy+12'] = frame3['United States of America'].shift(periods=-12)
frame3['UK Italy+13'] = frame3['United Kingdom'].shift(periods=-13)
frame3['Spain Italy+8'] = frame3['Spain'].shift(periods=-8)

# set the title
plt.title('COVID-19 Confirmed Cases')
plt.title('Log Scale', loc='left')
plt.title(date_title, loc='right')


# set x current axis with a logritmetic scale that greatly helps see the pace of exponential increase
ax = plt.gca()  
plt.yscale('log')

# based on the countries list: construct the graph
for i, country in enumerate(countries): 
    frame3.plot(kind='line', x='Days from Today', y=country, color=colors[i], ax=ax)

# show it
plt.show()
