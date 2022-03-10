from itertools import permutations
from django.shortcuts import render
from django.http import HttpResponse
from abc import ABC, abstractmethod

class Communication(ABC):
    pass

class PushCommunication:
    pass

# Create your views here.
def main(request):

    # return HttpResponse("kamo")

    return HttpResponse("<h1>jarda<h1>")



