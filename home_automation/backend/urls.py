from .views import  NetworkPushCommunication, testing_function, home, update_device, Export, add_rooms, add_device
from django.urls import path

urlpatterns = [
    # testing function
    # --------
    path("test/", testing_function),

    # URLS for communication with server-side frontend
    # --------
    path('', home, name="home"),     # server-side frontend dashboard path
    path('add_rooms/', add_rooms, name="add_rooms"),   # add new room path  
    path('add_device/<device_type>', add_device, name="add_device"),    # add new device specified via arguments path
    path('update_device/<device_id>/<device_type>', update_device, name="update-device"),   # update correct device specified via id and device type in arguments
    path('export/', Export.as_view(), name="export"),   # showing export form

    # URLS for PUSH communication with devices
    # --------
    path("push/", NetworkPushCommunication.as_view()),      # data insides URL parametres (GET) 
    path("push/<name>/<delimiter>/", NetworkPushCommunication.as_view(), name="name"),      # for data inside HTTP, name can be csv/parametres and delimiter ;/,/& (POST)
]
