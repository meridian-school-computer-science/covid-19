import csv

path = 'C:\\Users\\k_mac\\OneDrive\\Meridian\\h Computer Science\\Teacher Projects\\COVID\\data\\usa facts\\'
cases_filename = 'covid_confirmed_usafacts.csv'
deaths_filename = 'covid_deaths_usafacts.csv'
population_filename = 'covid_county_population_usafacts.csv'
county_location_filename = '2019_Gaz_counties_national_lat_lon.csv'

data = []
with open(path+county_location_filename, newline='',) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append(row)

print(data)

# encoding='utf-8-sig'