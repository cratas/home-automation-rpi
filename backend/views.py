from itertools import permutations
from django.shortcuts import render
from django.http import HttpResponse
import requests


from .helpers.communication import *


# Create your views here.
def main(request):

    communication = NetworkPullCommunication("https://pastebin.com/raw/YpAhDHBa")
    data = communication.send_data_request()

    return HttpResponse(data)



