from django.http import HttpResponse
from django.views import View
from abc import ABC, abstractmethod
import csv
from django.views.generic import DetailView

from .models import *
 
 
# Create your views here.
def main(request):
    return HttpResponse("Works")
 
# --------------
# PARSER CLASSES
# --------------
class Parser(ABC):
    def __init__(self, data):
        self.data = data
 
    @abstractmethod
    def parse_into_dict(self):
        pass
 
    def is_number(self, sample_str):
        result = True
        try:
            float(sample_str)
        except:
            result = False
        return result
 
    def process_data(self, data=None):
        pass
        if data is None:
            data = self.data
 
        if data is None:
            return False
 
        if data["id"] is None:
            return False
        else:
            device_id = data["id"]
 
        device = PushDevice.objects.get(identifier=device_id)
        values_list = DeviceValuesList.objects.create(device=device)
 
        for key, value in data.items():
            if key == 'id':
                continue
 
            if "," in value:
                value = value.replace(',','.')
 
            if self.is_number(value):
                NumericValueObject.objects.create(value_title=key, value=value, device_values=values_list)
            else:
                StringValueObject.objects.create(value_title=key, value=value, device_values=values_list)
 
        return True
 
 
 
class ParametresParser(Parser):
    def parse_into_dict(self):
        self.data = dict(x.split("=") for x in self.data.split("&"))
 
 
class CSVParser(Parser):
 
    def __init__(self, data, delimiter):
        Parser.__init__(self, data)
        self.delimiter = delimiter
 
    def process_data(self):
        for incoming_values in self.data:
            if super().process_data(incoming_values) is False:
                return False
 
        return True
 
 
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

# --------------
# COMMUNICATION CLASSES
# --------------
# class PushCommunication():
#     def __init__(self):
#         self.parser_type=None

class NetworkCommunication(DetailView):
    slug = None

    def get_object(self, queryset=None):
        return queryset.get(slug=self.slug)


    def get(self, request, *args, **kwargs):
        self.parser_type = kwargs['name']

        retrieved_data = request.GET
 
        if not retrieved_data:
            return HttpResponse("Data NOT inserted into database")
 
        parser = ParserFactory(self.parser_type, retrieved_data, ',')

        if parser.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")
 
    def post(self, request, *args, **kwargs):
        self.parser_type = kwargs['name']
        retrieved_data = request.body.decode('utf-8')
 
        if not retrieved_data:
            return HttpResponse("Data NOT inserted into database")
 
        parser = ParserFactory.get_instance().create_parser(self.parser_type, retrieved_data, ',')
        
        parser.parse_into_dict()
 
        if parser.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")


class SerialBusCommunication():
    pass
