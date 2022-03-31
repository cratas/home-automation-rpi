from django.urls import path
from .views import  NetworkPushCommunication, testing_function, home, update_device, Export, add_rooms, add_device

urlpatterns = [
    #rendering home site
    path('', home, name="home"),
    path('add_rooms/', add_rooms, name="add_rooms"),
    path('add_device/<device_type>', add_device, name="add_device"),
    path('update_device/<device_id>/<device_type>', update_device, name="update-device"),
    path('export/', Export.as_view(), name="export"),
    
    #--------
    # URLS for PUSH communication with devices
    #--------
    #for data insides URL parametres (GET)
    path("push/", NetworkPushCommunication.as_view()),
    #for data inside http, name can be csv/parametres and delimiter ;/,/& (POST)
    path("push/<name>/<delimiter>/", NetworkPushCommunication.as_view(), name="name"),
    
    path("test/", testing_function),
]
