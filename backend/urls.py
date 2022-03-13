from django.urls import path
from .views import main, NetworkCommunication

urlpatterns = [
    path('home', main),
    path('about/', NetworkCommunication.as_view()),
]