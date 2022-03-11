from itertools import permutations
from django.shortcuts import render
from django.http import HttpResponse

import requests


from .helpers.communication import *
from .helpers.cash import *



# Create your views here.
def main(request):

    # communication = NetworkPullCommunication("https://pastebin.com/raw/Az8Jr8GC")
    # data = communication.send_data_request()

    CashMemory.add_device('tonda')
    CashMemory.add_device('milan')
    

    for item in CashMemory.devices: print(item)

    return HttpResponse("sdf")



