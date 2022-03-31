from django.urls import path
from .views import DashboardView, RoomsView


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('rooms/', RoomsView.as_view(), name="rooms"),

]