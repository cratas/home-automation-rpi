from django.urls import path
from .views import main, NetworkCommunication

urlpatterns = [
    path('home/', main),
    path('about/', NetworkCommunication.as_view()),
    path('push/csv/', NetworkCommunication.as_view('CSV')),
    path('push/parametres/', NetworkCommunication.as_view('PARAMETRES')),

]