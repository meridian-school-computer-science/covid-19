#https://covidtracking.com/api

import pandas as pd
import csv
from matplotlib import pyplot as plt
import datetime as dt



date_title = '16 May'


class Settings:

    def __init__(self):
        self.path = 'C:\\Users\\k_mac\\OneDrive\\Meridian\\h Computer Science\\Teacher Projects\\COVID\\data\\usa facts\\'
        self.cases_filename = 'covid_confirmed_usafacts.csv'
        self.deaths_filename = 'covid_deaths_usafacts.csv'
        self.population_filename = 'covid_county_population_usafacts.csv'
        self.county_location_filename = '2019_Gaz_counties_national_lat_lon.csv'
        self.states = ['California', 'Texas', 'Florida', 'New York', 'Pennsylvania', 'Illinois', 'Ohio', 'Georgia', 'North Carolina',
                        'Michigan', 'New Jersey', 'Virginia', 'Washington', 'Arizona', 'Massachusetts', 'Tennessee', 'Indiana',
                        'Missouri', 'Maryland', 'Wisconsin', 'Colorado', 'Minnesota', 'South Carolina', 'Alabama', 'Louisiana', 
                        'Kentucky', 'Oregon', 'Oklahoma', 'Connecticut', 'Utah', 'Puerto Rico', 'Iowa', 'Nevada', 'Arcansas',
                        'Mississippi', 'Kansas', 'New Mexico', 'Nebraska', 'West Virginia', 'Idaho', 'Hawaii', 'New Hampshire',
                        'Maine', 'Montana', 'Rhode Island', 'Delaware', 'South Dakota', 'North Dakota', 'Alaska', 'District of Columbia',
                        'Vermont', 'Wyoming', 'Guam', 'U.S. Virgin Islands', 'American Samoa']
        self.state_abbreviation = [ 'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
                                    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
                                    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
                                    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
                                    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC']
        self.death_rate_adjustment = 250


class DataReader:

    def __init__(self, path):
        self.path = path
        self.filename = ''
        self.data = []

    def read_file(self, filename, encode=True):
        self.filename = filename
        if encode:
            self.load_data_utf()
        else:
            self.load_data()

    def load_data_utf(self):
        self.data = []
        with open(self.path+self.filename, newline='',encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append(row)

    def load_data(self):
        self.data = []
        with open(self.path+self.filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append(row)

    def get_data(self):
        return self.data


class AllStates:

    def __init__(self):
        self.items = dict()

    def add_state(self, code, state):
        self.items[code] = State(state)


class State:

    def __init__(self, details):
        self.details = details
        

class AllCounties:

    def __init__(self):
        self.items = dict()

    def add_county(self, id_, county):
        self.items[id_] = county

    def __str__(self):
        build = ''
        for each_county in self.items.values():
            build = build + str(each_county) + '\n'
        return build


class County:

    def __init__(self, id_, name, state, population):
        self.id_ = id_
        self.name = name
        self.state = state
        self.population = population
        self.lat = 0.0
        self.lon = 0.0
        self.date_data = {}

    def add_date_data(self, date, details):
        self.date_data[date] = details

    def __str__(self):
        return f"{self.id_}: {self.name}, {self.state}. ({self.lat}, {self.lon}). Pop: {int(self.population):,}"


class DateData:

    def __init__(self):
        self.date = ''
        self.confirmed = ''
        self.deaths = ''

    def get_date_details(self):
        return (self.date, {'confirmed': self.confirmed, 'deaths': self.deaths})


class RawData():

    def __init__(self, reader, controller):
        self.reader = reader
        self.controller = controller
        self.population_data = []
        self.case_data = []
        self.death_data = []
        self.county_location = []

    def get_all_data(self):
        self.reader.read_file(self.controller.settings.population_filename)
        self.population_data = self.reader.get_data()

        self.reader.read_file(self.controller.settings.cases_filename)
        self.case_data = self.reader.get_data()

        self.reader.read_file(self.controller.settings.deaths_filename)
        self.death_data = self.reader.get_data()

        self.reader.read_file(self.controller.settings.county_location_filename, False)
        self.county_location = self.reader.get_data()


class DataParser:

    def __init__(self, raw_data, all_states, all_counties):
        self.raw_data = raw_data
        self.all_states = all_states
        self.all_counties = all_counties
        self.county_codes = []
        

    def build_models(self):
        texas_pop = []
        for each in self.raw_data.population_data:
            if each['State'] == 'TX':
                texas_pop.append(each)
                self.county_codes.append(each['countyFIPS'])
        for each in texas_pop:
            each_county = County(each['countyFIPS'], each['County Name'], each['State'], each['population'])
            self.all_counties.add_county(each['countyFIPS'], each_county)
        self.add_county_location_details()
        print(self.county_codes)

    def add_county_location_details(self):
        texas_location = {}
        for each in self.raw_data.county_location:
            if each['USPS'] == 'TX':
                texas_location[each['GEOID']] = (each['LAT'], each['LON'])
        for k, v in texas_location.items():
            self.all_counties.items[k].lat = v[0]
            self.all_counties.items[k].lon = v[1]



class Controller:

    def __init__(self):
        self.settings = Settings()
        self.reader = DataReader(self.settings.path)
        self.raw_data = RawData(self.reader, self)
        self.all_states = AllStates()
        self.all_counties = AllCounties()
        self.parser = DataParser(self.raw_data, self.all_states, self.all_counties)
        self.get_all_data()
        self.build_models()

    def get_all_data(self):
        self.raw_data.get_all_data()

    def build_models(self):
        self.parser.build_models()


    

my_controller = Controller()