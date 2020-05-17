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
        self.data = {}

    def read_file(self, filename):
        self.filename = filename
        self.load_data()

    def load_data(self):
        with open(self.path+self.filename, newline='',encoding='utf-8-sig') as csvfile:
            self.data = csv.DictReader(csvfile)

    def get_data(self):
        return self.data



