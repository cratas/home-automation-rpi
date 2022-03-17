from django.urls import path
from .views import  NetworkPushCommunication, testing_function

urlpatterns = [
    #for data insides URL parametres
    path("push/", NetworkPushCommunication.as_view()),
    #for data inside http (CSV, or PARAMETRES)
    path("push/<name>/", NetworkPushCommunication.as_view(), name="name"),
    path("test/", testing_function),
]