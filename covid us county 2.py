#https://covidtracking.com/api

#import pandas as pd
import csv
import copy
import datetime
from matplotlib import pyplot as plt




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
        self.colors =    [ "red",  "black", "purple", 
                            "blue", "magenta", "orange",
                            "yellow", "green"]
        self.death_rate_adjustment = 250


class DataReader:

    def __init__(self, path):
        self.path = path
        self.filename = ''
        self.data = {}

    def read_file(self, filename, id_, encode=True):
        self.filename = filename
        self.data = {}
        if encode:
            self.load_data_utf(id_)
        else:
            self.load_data(id_)

    def load_data_utf(self, id_):
        with open(self.path+self.filename, newline='',encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data[row[id_]] = row

    def load_data(self, id_):
        with open(self.path+self.filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data[row[id_]] = row

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
        self.non_dates = ['countyFIPS', 'County Name', 'State', 'stateFIPS', 'GEOID']

    def get_date_details(self):
        return (self.date, {'confirmed': self.confirmed, 'deaths': self.deaths})

        #format for date records: 
        # key is date :: date time group obj
        # value is dictionary of: key : values -> 'confirmed' : int, 'deaths' : int
        # can we get data on hospitalizations by county? 
        # can we get testing data by county?

    def clear_non_data(self, raw_dict):
        selected_keys = list()
        working = copy.deepcopy(raw_dict)
        # remove key:value for non-date tuples
        # convert date to a dtg (make sure it is ok for that to be a key)
        # add to a temp dictionary key=data, value(dictionary) or a list?
        for k in working.keys():
            if k in self.non_dates:
                selected_keys.append(k)
        
        for each_k in selected_keys:
            del working[each_k]
        return working


class RawData():

    def __init__(self, reader, controller):
        self.reader = reader
        self.controller = controller
        self.population_data = {}
        self.case_data = {}
        self.death_data = {}
        self.county_location = {}

    def get_all_data(self):
        self.reader.read_file(self.controller.settings.population_filename, 'countyFIPS')
        self.population_data = self.reader.get_data()

        self.reader.read_file(self.controller.settings.cases_filename, 'countyFIPS')
        self.case_data = self.reader.get_data()

        self.reader.read_file(self.controller.settings.deaths_filename, 'countyFIPS')
        self.death_data = self.reader.get_data()

        self.reader.read_file(self.controller.settings.county_location_filename, 'GEOID', False)
        self.county_location = self.reader.get_data()



class DataParser:

    def __init__(self, raw_data, all_states, all_counties):
        self.raw_data = raw_data
        self.all_states = all_states
        self.all_counties = all_counties
        self.date_data = DateData()
        self.county_codes = []
        self.state_interest = ['TX']
        self.county_interest = ['48491', '48453']
        self.filtered_data = dict()
        self.map_data = dict()
        self.graph_data = dict()
        

    def set_filtered_data(self, filters={'counties':['48491', '48453']}):
        self.county_interest = filters['counties']
        self.filtered_data = dict()
        #filter by countyFIPS
        for each_county in self.county_interest:
            for key, value in self.raw_data.population_data.items():
                if value['countyFIPS'] == each_county:
                    self.county_codes.append(key)      


        #filter by state
        # for each_state in self.state_interest:
        #     for key, value in self.raw_data.population_data.items():
        #         if value['State'] == each_state:
        #             self.county_codes.append(key)

        # get rid of all 0
        done = False
        while not done:
            try:
                self.county_codes.remove('0')
            except:
                done = True

        for each_county in self.county_codes:
            one_county = {
                'County Name' : self.raw_data.population_data[each_county]['County Name'],
                'State' : self.raw_data.population_data[each_county]['State'],
                'Population' : self.raw_data.population_data[each_county]['population'], 
                'LAT' : self.raw_data.county_location[each_county]['LAT'],
                'LON' : self.raw_data.county_location[each_county]['LON']
            }
            self.filtered_data[each_county] = one_county


    def set_mapping_data(self):
        self.set_filtered_data()
        self.map_data = self.filtered_data

    def set_graphing_data(self):
        self.graph_data = self.filtered_data    
        temp_data = dict()
        for key in self.graph_data.keys():
            temp_data[key] = dict()
            temp_cases = self.raw_data.case_data[key]
            temp_deaths = self.raw_data.death_data[key]
            temp_data[key]['Cases'] = temp_cases
            temp_data[key]['Deaths'] = temp_deaths
           
        print(temp_data)


        # I need to stay with temp data and clear the other not date stuff first
        for k, v in temp_data.items():

            self.graph_data[k]['Cases'] = self.convert_details_to_dict(v['Cases'])
            self.graph_data[k]['Deaths'] = self.convert_details_to_dict(v['Deaths'])

        print(self.graph_data)
        #     temp_data[k] = self.date_data.clear_non_data(v)
        #     print(temp_data[k])

        # for k, v in temp_data.items():
        #     print(f"Key {k} : {v}")


    def convert_details_to_dict(self, details):
        working = dict()
        for county_key in details.keys():
            county_working = dict()
            for k, v in details[county_key].items():
                date_key = datetime.datetime.strptime(k, '%m/%d/%y')
                county_working[date_key] = int(v)
            working[county_key] = county_working
        return working  



class Graph:

    def __init__(self):
        self.settings = Settings()
        self.style = 'line'
        self.main_title = 'Test Graph'
        self.left_title = 'Log Scale'
        self.right_title = 'dates'
        self.yscale = 'log'
        self.series = list()
        self.dates = list()
        self.values = list()

    def set_graph(self, graph_data):
        self.series = list(graph_data.keys())
        self.dates = list(graph_data['48453'].keys())
        self.values = list(graph_data['48453'].values())
        print(self.series)
        plt.title(self.main_title)
        plt.title(self.left_title, loc='left')
        plt.title(self.right_title, loc='right')
        ax = plt.gca()
        plt.yscale(self.yscale)

        for i, line_plot in enumerate(self.series):
            plt.plot(self.dates, 
                    self.values, color=self.settings.colors[i])
        plt.show()



class Controller:

    def __init__(self):
        self.settings = Settings()
        self.reader = DataReader(self.settings.path)
        self.raw_data = RawData(self.reader, self)
        self.all_states = AllStates()
        self.all_counties = AllCounties()
        self.parser = DataParser(self.raw_data, self.all_states, self.all_counties)
        self.grapher = Graph()
        self.get_all_data()
        self.filter_data()
        self.display_graph()

    def get_all_data(self):
        self.raw_data.get_all_data()

    def filter_data(self):
        self.parser.set_mapping_data()
        self.parser.set_graphing_data()


    def display_graph(self):
        self.grapher.set_graph(self.parser.graph_data)

    

my_controller = Controller()