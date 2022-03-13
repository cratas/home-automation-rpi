from django.http import HttpResponse
from django.views import View

from .models import TestingDevice, TestingValueObject

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
            for key, value in retrieved_data.items():
                if key == 'id':
                    continue

                device = TestingDevice.objects.get(identifier=device_id)
                TestingValueObject.objects.create(value_name=key, value=value, device=device)

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


