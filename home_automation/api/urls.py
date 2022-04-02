from django.urls import path
from .views import DashboardView, RoomsView, ExportView, StatisticView


urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('rooms/', RoomsView.as_view(), name="rooms"),
    path('export/', ExportView.as_view(), name="export_frontend"),
    path('statistics/', StatisticView.as_view(), name="statistics"),
]