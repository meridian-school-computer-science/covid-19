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

    def read_file(self, filename):
        self.filename = filename
        self.load_data()

    def load_data(self):
        self.data = []
        with open(self.path+self.filename, newline='',encoding='utf-8-sig') as csvfile:
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


class DateData:

    def __init__(self):
        self.date = ''
        self.confirmed = ''
        self.deaths = ''

    def get_date_details(self):
        return (self.date, {'confirmed': self.confirmed, 'deaths': self.deaths})





class RawData():

    def __init__(self, reader):
        self.reader = reader
        self.population_data = []
        self.case_data = []
        self.death_data = []
        self.county_location = []

    def get_all_data(self):
        self.reader.read_file(self.settings.population_filename)
        self.population_data = self.reader.get_data()

        self.reader.read_file(self.settings.cases_filename)
        self.case_data = self.reader.get_data()

        self.reader.read_file(self.settings.deaths_filename)
        self.death_data = self.reader.get_data()

        self.reader.read_file(self.settings.county_location_filename)
        self.county_location = self.reader.get_data()


class DataParser:

    def __init__(self, raw_data, all_states, all_counties):
        self.raw_data = raw_data
        self.all_states = all_states
        self.all_counties = all_counties

    def build_models(self):
        pass



class Controller:

    def __init__(self):
        self.settings = Settings()
        self.reader = DataReader(self.settings.path)
        self.raw_data = RawData(self.reader)
        self.all_states = AllStates()
        self.all_counties = AllCounties()
        self.parser = DataReader(self.raw_data, self.all_states, self.all_counties)
        self.get_all_data()
        self.build_models()

    def get_all_data(self):
        self.raw_data.get_all_data()

    def build_models(self):
        self.parser.build_models()


    

my_controller = Controller()