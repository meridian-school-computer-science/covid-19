import csv, math


class DataReader:

    def __init__(self, filename):
        self.filename = filename
        self.data = []

    def read(self):

        with open(self.filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.data.append(row)



class CountryList:

    def __init__(self):
        self.interested = ['Worldwide', 'China', 'Italy', 'United States of America']     
        self.data = {}

    def build_data(self):
        pass

    def __str__(self):
        build = 'Country List:\n'
        for key, value in self.data.items():
            build += f"{self.data[key]}\n"
        return build

class Country:

    def __init__(self, name):
        self.name = name
        self.data = list()

    def add_date_data(self, date, cases):
        if cases == 'null':
            cases = 0
        self.data.append({'date': date, 'cases': cases})

    def __str__(self):
        build = self.name +'\n'
        for line in self.data:
            build += f"{line['date']}: {line['cases']}\n"
        return build


class DataParser:

    def __init__(self):
        pass

    def get_data(self):
        temp = []

class Controller:

    def __init__(self):
        self.reader = DataReader('data-00wGO.csv')
        self.parser = DataParser()
        self.country_list = CountryList()

        self.start()
        print(self.country_list)

    def start(self):
        self.reader.read()
        for country in self.country_list.interested:
            new_country = Country(country)
            
            for row in self.reader.data:
                new_country.add_date_data(row['date'], row[country])
            
            self.country_list.data[country] = new_country
            



controller = Controller()