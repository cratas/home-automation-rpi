from django.http import HttpResponse
from django.views import View

from .models import Room, Device, DeviceValuesList, BaseValueObject, StringValueObject, NumericValueObject, BooleanValueObject

# from .models import OneValueDevice, ValueObject

from .helpers.communication import *
from .helpers.cash import *
from rest_framework import generics

# Create your views here.
def main(request):
    return HttpResponse("Works")

class NetworkCommunication(View):
    def save_data(self, retrieved_data={}):
        device_id = retrieved_data["id"]
        if device_id is None:
            return False

        if retrieved_data is not None:
            device = Device.objects.get(identifier=device_id)
            values_list = DeviceValuesList.objects.create(device=device)

            for key, value in retrieved_data.items():
                if key == 'id':
                    continue


                if type(value) == str:
                    StringValueObject.objects.create(value_title=key, value=value, device_values=values_list)


                print(f'{key} : {value}')

        return True

    def get(self, request):
        retrieved_data = request.GET

        if self.save_data(retrieved_data) is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into databae")


    def post(self, request):
        retrieved_data = request.body.decode('utf-8')
        retrieved_data = dict(x.split("=") for x in retrieved_data.split("&"))

        if self.save_data(retrieved_data) is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into databae")


