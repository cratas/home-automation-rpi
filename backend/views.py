from itertools import permutations
from django.shortcuts import render
from django.http import HttpResponse

import requests

from .models import OneValueDevice, ValueObject

from .helpers.communication import *
from .helpers.cash import *



# Create your views here.
def main(request):

    # communication = NetworkPullCommunication("https://pastebin.com/raw/Az8Jr8GC")
    # data = communication.send_data_request()
    
    temp_sensor = OneValueDevice.objects.get(device_name="tempSensor")
    ValueObject.objects.create(value_name="tempr", value="42", device=temp_sensor)


    return HttpResponse("Works")



