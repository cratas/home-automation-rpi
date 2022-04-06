from .views import DashboardView, RoomsView, ExportView, StatisticView, DeviceStatus, TemperatureStatisticView, DeviceStatisticsView
from django.urls import path

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),     # main frontend dashboard path
    path('rooms/', RoomsView.as_view(), name="rooms"),     # path for getting all rooms data 
    path('export/', ExportView.as_view(), name="export_frontend"),    # path for export functionality
    path('device/status/', DeviceStatus.as_view(), name="device_status"),   # path for getting all devices with status
    path('statistics/', StatisticView.as_view(), name="statistics"),    # path for getting last month consumption data
    path('statistics/values/', TemperatureStatisticView.as_view(), name="statistics_values"),    # path for getting temperature and humidity for specific room
    path('statistics/device/', DeviceStatisticsView.as_view(), name="statistic_device"),       # parth for getting all data for specific device and specific interval
]

