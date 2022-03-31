from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import *


# Create your views here.
class DashboardView(APIView):
    def get(self, request):
        house_temperature = self.count_avg('temperature')
        house_humidity = self.count_avg('humidity')
        # house_co2 = self.count_avg('co2')
        rooms_info = []

        for room in Room.objects.all():
            room = {
                'name': room.name,
                'active_count': room.get_active_dev_count(),
                'non_active_count': room.get_non_active_dev_count(),
                'error_count': room.any_device_has_error()
            }
            rooms_info.append(room)

        return Response({'house_temperature': house_temperature, 'house_humidity': house_humidity, 'rooms': rooms_info})

    # function to count specific value for whole house (all rooms avg)
    def count_avg(self, value_type):
        rooms_values = []

        # there should be iteration over active devices only
        for device in Device.objects.all():
            try:
                for v in device.get_last_value().get_values().filter(value_title=value_type):
                    rooms_values.append(v.value)
            except:
                pass

        return round(sum(rooms_values) / len(rooms_values))


class RoomsView(APIView):
    def get(self, request):
        rooms_values = []

        for room in Room.objects.all():
            room_dict = {}
            room_dict['name'] = room.name

            devices_list = []
            for device in Device.objects.filter(room=room):
                device_dict = {'name' : device.device_name, 'last_time' : device.get_last_communication_time(), 'is_active' : device.is_active, 'has_error' : device.has_error }
                devices_list.append(device_dict)
                try:
                    room_dict['temperature'] = round(device.get_last_value().get_values().filter(value_title='temperature').first().value)
                    room_dict['humidity'] = round(device.get_last_value().get_values().filter(value_title='humidity').first().value)
                    # room_dict['co2'] = round(device.get_last_value().get_values().filter(value_title='co2').first().value)
                except:
                    pass

            room_dict['devices'] = devices_list
            rooms_values.append(room_dict)

        return Response(rooms_values)
