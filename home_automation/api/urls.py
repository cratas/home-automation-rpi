from django.urls import path
from .views import DashboardView, RoomsView, ExportView, StatisticView, DeviceStatus, TemperatureStatisticView, DeviceStatisticsView

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name="dashboard"),
    path('rooms/', RoomsView.as_view(), name="rooms"),
    path('export/', ExportView.as_view(), name="export_frontend"),
    path('device/status/', DeviceStatus.as_view(), name="device_status"),
    path('statistics/', StatisticView.as_view(), name="statistics"),
    path('statistics/values/', TemperatureStatisticView.as_view(), name="statistics_values"),
    path('statistics/device/', DeviceStatisticsView.as_view(), name="statistic_device"),
]

