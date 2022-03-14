from django.http import HttpResponse
from django.views import View
from abc import ABC, abstractmethod
import re    

from .helpers import *
from .models import *

from .helpers.communication import *
from .helpers.cash import *

# Create your views here.
def main(request):
    return HttpResponse("Works")




class Parser(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process_data(self):
        pass

    def is_number(self, sample_str):
        result = True
        try:
            float(sample_str)
        except:
            result = False
        return result

class NetworkParser(Parser):

    def parse_into_dict(self):
        self.data = dict(x.split("=") for x in self.data.split("&"))

    def process_data(self):
        device_id = self.data["id"]
        if device_id is None:
            return False

        if self.data is not None:
            device = Device.objects.get(identifier=device_id)
            values_list = DeviceValuesList.objects.create(device=device)

            for key, value in self.data.items():
                if key == 'id':
                    continue

                if super().is_number(value):
                    NumericValueObject.objects.create(value_title=key, value=value, device_values=values_list)
                else:
                    StringValueObject.objects.create(value_title=key, value=value, device_values=values_list)

        return True


class NetworkCommunication(View):

    def get(self, request):
        retrieved_data = request.GET
        parser = NetworkParser(retrieved_data)

        if parser.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into databae")

    def post(self, request):
        retrieved_data = request.body.decode('utf-8')
     
        parser = NetworkParser(retrieved_data)
        parser.parse_into_dict()

        if parser.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into databae")


