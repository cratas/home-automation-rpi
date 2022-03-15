from operator import delitem
from xml.dom.expatbuilder import parseFragmentString
from django.http import HttpResponse
from django.views import View
from abc import ABC, abstractmethod
import csv

from .helpers import *
from .models import *

from .helpers.communication import *
from .helpers.cash import *

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
        if data is None:
            data = self.data

        device_id = data["id"]
        if device_id is None:
            return False

        if data is not None:
            device = Device.objects.get(identifier=device_id)
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



class NetworkParser(Parser):
    def parse_into_dict(self):
        self.data = dict(x.split("=") for x in self.data.split("&"))


class CSVParser(Parser):
    def parse_into_dict(self):
        #parsing csv file via csv library into dict
        data_lines = self.data.splitlines()
        file_data=csv.reader(data_lines, delimiter=',')

        #getting csv headers
        headers=next(file_data)
        #creating dict from csv file
        self.data = [dict(zip(headers,i)) for i in file_data]
        self.data = self.data[0]


class PLCParser(Parser):

    def __init__(self, data):
        Parser.__init__(self, data)
        self.data_list = []


    def process_data(self):
        for incoming_values in self.data_list:
            super().process_data(incoming_values)

    def parse_into_dict(self):
        #parsing csv file via csv library into dict
        data_lines = self.data.splitlines()
        file_data=csv.reader(data_lines, delimiter=';')

        #getting csv headers
        headers=next(file_data)
        #creating list of dicts from csv file
        self.data_list  = [dict(zip(headers,i)) for i in file_data]
        # print(self.data_list)

# --------------
# COMMUNICATION CLASSES
# --------------
class NetworkCommunication(View):

    def get(self, request):
        retrieved_data = request.GET

        if not retrieved_data:
            return HttpResponse("Data NOT inserted into database")
        
        parser = NetworkParser(retrieved_data)

        if parser.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")

    def post(self, request):
        retrieved_data = request.body.decode('utf-8')

        if not retrieved_data:
            return HttpResponse("Data NOT inserted into database")

        parser = PLCParser(retrieved_data)
        # parser = CSVParser(retrieved_data)
        #parser = NetworkParser(retrieved_data)
        parser.parse_into_dict()


        if parser.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")


