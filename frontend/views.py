from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView



# Create your views here.
def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html')
