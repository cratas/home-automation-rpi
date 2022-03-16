from django.urls import path
from .views import main, NetworkPushCommunication

urlpatterns = [
    path('home/', main),
    path("push/", NetworkPushCommunication.as_view()),
    path("push/<name>/", NetworkPushCommunication.as_view(), name="name"),
]