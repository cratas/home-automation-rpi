from django.http import HttpResponse
from django.views import View

import requests

# from .models import OneValueDevice, ValueObject

from .helpers.communication import *
from .helpers.cash import *
from rest_framework import generics




# Create your views here.
def main(request):

    return HttpResponse("Works")



class NetworkCommunication(generics.ListAPIView):

    def get(self, request):
        params = request.META['QUERY_STRING']

        if params is not None:
            return HttpResponse(params)
        return HttpResponse("BAD")

    def post(self, request):
        data = request.body.decode('utf-8')

        return HttpResponse(data)


