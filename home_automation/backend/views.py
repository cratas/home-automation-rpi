from django.http import HttpResponse
from django.views import View
from abc import ABC, abstractmethod
import csv
 
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
# COMMUNICATION CLASSES
# --------------
class NetworkCommunication(View):
 
    def get(self, request):
        retrieved_data = request.GET
 
        if not retrieved_data:
            return HttpResponse("Data NOT inserted into database")
 
        parser = ParametresParser(retrieved_data)
 
        if parser.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")
 
    def post(self, request):
        retrieved_data = request.body.decode('utf-8')
 
        if not retrieved_data:
            return HttpResponse("Data NOT inserted into database")
 
        # parser = ParametresParser(retrieved_data)
 
        parser = CSVParser(retrieved_data, ',')
        parser.parse_into_dict()
 
        print(Device.objects.all())
 
        if parser.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")
