from abc import ABC, abstractmethod
from django.http import QueryDict
import csv

# --------------
# PARSER CLASSES
# --------------
class Parser(ABC):
    def __init__(self, data):
        self.data = data
 
    @abstractmethod
    def parse_into_dict(self):
        pass

# --------------
# class for parsing data in parametres format
# --------------
class ParametresParser(Parser):

    # method for parse incoming data from HTTP request into dict
    def parse_into_dict(self):
        # checking if incoming data are already dict
        if isinstance(self.data, QueryDict):
            self.data = [ self.data.dict() ]
        # otherwice dict will be created
        else:
            self.data = [ dict(x.split("=") for x in self.data.split("&")) ]

        return self.data
# --------------
# class for parsing data in csv format
# --------------
class CSVParser(Parser):
 
    def __init__(self, data, delimiter):
        Parser.__init__(self, data)
        self.delimiter = delimiter
 
    def parse_into_dict(self):
        # parsing csv file via csv library into dict
        data_lines = self.data.splitlines()
        file_data=csv.reader(data_lines, delimiter=self.delimiter)
 
        # getting csv headers
        headers=next(file_data)
        # creating dict from csv file
        self.data = [dict(zip(headers,i)) for i in file_data]

        return self.data

# --------------
# SINGLETON Class for creating specific type of parser
# --------------
class ParserFactory:
    __instance = None

    @staticmethod
    def get_instance():
        if ParserFactory.__instance == None:
            ParserFactory()
        return ParserFactory.__instance

    def __init__(self):
        if ParserFactory.__instance != None:
            raise Exception("This class is singleton!")
        else:
            ParserFactory.__instance = self

    # creating appropriate typee of parser by method parametres
    def create_parser(self, type, data, delimiter=','):
        if type == 'csv':
            parser = CSVParser(data, delimiter)
            return parser
        elif type == 'parametres':
            parser = ParametresParser(data)
            return parser
        else:
            raise Exception("Unknown type of data format")

# help function used for recognize incoming data
def is_number(sample_str):
    result = True
    try:
        float(sample_str)
    except:
        result = False
    return result
