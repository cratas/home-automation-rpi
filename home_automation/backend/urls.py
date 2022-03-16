from django.urls import path
from .views import main, NetworkCommunication

urlpatterns = [
    path('home/', main),
    # path('push/csv/', NetworkCommunication.as_view('CSV')),
    # path('push/parametres/', NetworkCommunication.as_view(slug='PARAMETRES')),
    path("push/<name>/", NetworkCommunication.as_view(), name="name"),
]