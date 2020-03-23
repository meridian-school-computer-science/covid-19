import pandas as pd
import csv
from matplotlib import pyplot as plt
import datetime as dt

path = 'C:\\Users\\k_mac\\OneDrive\\Meridian\\h Computer Science\\Teacher Projects\\COVID\\'
# old example: filename = 'data-00wGO.csv'
filename = 'total_cases_current.csv'
# Datasource: https://ourworldindata.org/coronavirus-source-data

frame = pd.read_csv(path+filename)
frame.fillna(0)

frame2 = pd.DataFrame(frame, columns=['date', 'Worldwide', 'Italy', 'France', 'Germany', 'United States of America'])
frame2.fillna(0)

countries = ['Italy', 'France Italy+x', 'Germany', 'United States of America', 'Denmark', 'Japan']
colors =    [ "red",  "blue",   "green",    "black",                  "purple",   "orange",  "yellow" , "magenta"]
offset = [0, 7, 5, 6, 12, -25]
reference_date = pd.Timestamp.today()

frame['date'] = pd.to_datetime(frame.date, format='%d-%m-%y')
frame3 = pd.DataFrame(frame, columns=['date', 'Italy', 'France', 'Germany', 'United States of America', 'Denmark', 'Japan'])
frame3['Difference'] = frame3['date'].sub(reference_date).dt.days
frame3['France Italy+x'] = frame3['France'].sub(offset[1])

frame3.fillna(0)
frame3['Difference'] = frame3['date'].sub(reference_date).dt.days
frame3['France Italy+x'] = frame3['France'].sub(offset[1])

ax = plt.gca()  # get current axis
plt.yscale('log')
for i, country in enumerate(countries): 
    frame3.plot(kind='line', x='Difference', y=country, color=colors[i], ax=ax)

plt.show()