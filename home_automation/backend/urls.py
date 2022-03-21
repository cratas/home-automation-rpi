from django.urls import path
from .views import  NetworkPushCommunication, testing_function, home, rooms, devices, update_device, Export

urlpatterns = [


    path('', home, name="home"),
    path('rooms/', rooms, name="rooms"),
    path('devices/', devices, name="devices"),
    path('update_device/<device_id>/<device_type>', update_device, name="update-device"),
    path('export/', Export.as_view(), name="export"),
    #--------
    # URLS for communication with devices
    #--------
    #for data insides URL parametres
    path("push/", NetworkPushCommunication.as_view()),
    #for data inside http (CSV, or PARAMETRES)
    path("push/<name>/", NetworkPushCommunication.as_view(), name="name"),
    path("test/", testing_function),
]