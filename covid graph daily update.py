# data from 22 March 2020

# https://ourworldindata.org/coronavirus-source-data


# github: https://github.com/owid/covid-19-data/tree/master/public/data/ecdc
# ecdc data:
# https://www.ecdc.europa.eu/en/publications-data/download-todays-data-geographic-distribution-covid-19-cases-worldwide

import pandas as pd
import csv
from matplotlib import pyplot as plt
import datetime as dt
path = 'C:\\Users\\k_mac\\OneDrive\\Meridian\\h Computer Science\\Teacher Projects\\COVID\\data\\global\\'
filename = 'total_cases_29_sep.csv'
date_title = '29 Sep'

# a change also from inside github

frame = pd.read_csv(path+filename)
#frame['date'] = pd.to_datetime(frame.date, format='%d-%m-%Y')
frame['date'] = pd.to_datetime(frame.date)

# Which Countries are we going to graph
#countries = ['Italy', 'France Italy+8', 'Germany Italy+8', 'USA Italy+12', 'Denmark Italy+14', 'UK Italy+13', 'Japan', 'Spain Italy+8' ]

countries = ['Italy', 'S. Korea Italy-3', 'Japan Italy-2', 
            'USA Italy+8', 'UK Italy+8','Spain Italy+8',
            'Sweden Italy+12', 'Denmark Italy+15'                
            ]
# others: 'FRA Italy+6', 'GER Italy+6'

colors =    [ "red",  "black", "purple", 
              "blue", "magenta", "orange",
             "yellow", "green"]

reference_date = pd.Timestamp.today()


frame3 = pd.DataFrame(frame, 
    columns=['date', 'Italy', 'France', 'Germany', 'United States', 
            'Denmark', 'Japan', 'United Kingdom', 'Spain', 
            'South Korea', 'Sweden'])
blank_rows = range(0, 54)
frame3.drop(blank_rows, inplace=True)


# for x axis
frame3['Days from Today'] = frame3['date'].sub(reference_date).dt.days


# manually adjust a Country's graph based on Italy
# these lines shift their data column so it will align with Italy graph at the point that their outbreak became a problem
# 
# looking for points where a country's graph drops off of Italy's line (note: Japan from the start, and Denmark)
# limitation on this graph is data based on each nation's testing (that varies)

frame3['France Italy+6'] = frame3['France'].shift(periods=-6)
frame3['Germany Italy+6'] = frame3['Germany'].shift(periods=-6)
frame3['Denmark Italy+15'] = frame3['Denmark'].shift(periods=-15)
frame3['USA Italy+8'] = frame3['United States'].shift(periods=-8)
frame3['UK Italy+8'] = frame3['United Kingdom'].shift(periods=-8)
frame3['Spain Italy+8'] = frame3['Spain'].shift(periods=-8)
frame3['S. Korea Italy-3'] = frame3['South Korea'].shift(periods=3)
frame3['Sweden Italy+12'] = frame3['Sweden'].shift(periods=-12)
frame3['Japan Italy-2'] = frame3['Japan'].shift(periods=2)

fig=plt.figure(figsize=(10,8))
# set the title
plt.title('COVID-19 Confirmed Cases')
plt.title('Log Scale', loc='left')
plt.title(date_title, loc='right')


# set x current axis with a logritmetic scale that greatly helps see the pace of exponential increase
ax = plt.gca()  
plt.yscale('log')
#plt.yscale('linear')

# based on the countries list: construct the graph
for i, country in enumerate(countries): 
    frame3.plot(kind='line', x='Days from Today', y=country, color=colors[i], ax=ax)

# show it
plt.show()
