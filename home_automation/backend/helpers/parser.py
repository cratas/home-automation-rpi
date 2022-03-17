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

class ParametresParser(Parser):
    def parse_into_dict(self):
        if isinstance(self.data, QueryDict):
            self.data = [ self.data.dict() ]
        else:
            self.data = [ dict(x.split("=") for x in self.data.split("&")) ]

class CSVParser(Parser):
 
    def __init__(self, data, delimiter):
        Parser.__init__(self, data)
        self.delimiter = delimiter
 
    def parse_into_dict(self):
        #parsing csv file via csv library into dict
        data_lines = self.data.splitlines()
        file_data=csv.reader(data_lines, delimiter=self.delimiter)
 
        #getting csv headers
        headers=next(file_data)
        #creating dict from csv file
        self.data = [dict(zip(headers,i)) for i in file_data]

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

    def create_parser(self, type, data, delimiter=','):
        if type == 'csv':
            parser = CSVParser(data, delimiter)
            return parser
        elif type == 'parametres':
            parser = ParametresParser(data)
            return parser
        else:
            raise Exception("Unknown type of data format")


def is_number(sample_str):
    result = True
    try:
        float(sample_str)
    except:
        result = False
    return result
