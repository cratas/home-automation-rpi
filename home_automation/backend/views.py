from django.http import HttpResponse
from django.views import View
from abc import ABC, abstractmethod
import csv
from django.views.generic import DetailView
from django.core.exceptions import ObjectDoesNotExist
import requests
from django.http import QueryDict

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


def get_data(source_address):
    try:
        response = requests.get(source_address,timeout=3)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as errh:
        return("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        return("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        return("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        return("OOps: Something Else", err)

def testing_function(rquest):

    for device in PullDevice.objects.all():

        retrieved_data = get_data(device.source_address)
        
        parser = ParserFactory.get_instance().create_parser(device.format, retrieved_data, ',')
        parser.parse_into_dict()
        parser.process_data()
        
        print(parser.data)

    return HttpResponse("OK")

# --------------
# COMMUNICATION CLASSES
# --------------
class PushCommunication():
    def __init__(self):
        self.parser_type='parametres'
        self.retreived_data = None

    def is_number(self, sample_str):
        result = True
        try:
            float(sample_str)
        except:
            result = False
        return result


    def process_data(self):

        #getting device id from incoming data
        device_identifier = self.retreived_data[0]["id"]

        #if device with incoming id does not exist, method will return False
        try:
            device = PushDevice.objects.get(identifier=device_identifier)
        except ObjectDoesNotExist:
            return False

        #iterate over all dicts in dict list
        for dict_object in self.retreived_data:
            values_list = DeviceValuesList.objects.create(device=device)

            #iterate over every dict inside list
            for key, value in dict_object.items():
                #ignore values with key id
                if key == 'id':
                    continue

                #convert to correct float format
                if "," in value:
                    value = value.replace(',','.')
    
                #creating correct type of value
                if self.is_number(value):
                    NumericValueObject.objects.create(value_title=key, value=value, device_values=values_list)
                else:
                    StringValueObject.objects.create(value_title=key, value=value, device_values=values_list)
 
        return True

class NetworkPushCommunication(PushCommunication, View):
    def get(self, request):
        #getting data via get request
        incoming_data = request.GET

        #checking if incoming data aren't null
        if not incoming_data:
            return HttpResponse("Data NOT inserted into database")
 
        #retrieved data are already represented as dic
        parser = ParserFactory.get_instance().create_parser(self.parser_type, incoming_data, ',')
        parser.parse_into_dict()

        self.retreived_data = parser.data

        #process data
        if self.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")

        return HttpResponse("Data NOT inserted into database")
 
    def post(self, request, *args, **kwargs):
        #specific format of incoming data
        self.parser_type = kwargs['name']
        #getting data via post request
        incoming_data = request.body.decode('utf-8')
 
        #checking if incoming data aren't null
        if not incoming_data:
            return HttpResponse("Data NOT inserted into database")
 
        #parsing retrieved data via parser
        parser = ParserFactory.get_instance().create_parser(self.parser_type, incoming_data, ',')
        parser.parse_into_dict()
 
        self.retreived_data = parser.data

        #process data
        if self.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")

        return HttpResponse("Data NOT inserted into database")


class SerialBusPushCommunication(PushCommunication):

    def __init__(self, trans_speed, trans_size, stop_bit):
        self.parser_type='csv'
        self.trans_speed = trans_speed
        self.trans_size = trans_size
        self.stop_bit = stop_bit

    def receive_data(self):
        pass
