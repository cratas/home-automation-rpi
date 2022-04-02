import re
from django.shortcuts import render
from graphviz import view
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import *
from django.http import HttpResponse
from django.views import View

# Create your views here.
class DashboardView(APIView):
    def get(self, request):
        house_temperature = self.count_avg('temperature')
        house_humidity = self.count_avg('humidity')
        house_co2 = self.count_avg('co2')

        rooms_info = []

        for room in Room.objects.all():
            room = {
                'name': room.name,
                'active_count': room.get_active_dev_count(),
                'non_active_count': room.get_non_active_dev_count(),
                'error_count': room.any_device_has_error()
            }
            rooms_info.append(room)

        return Response({'house_temperature': house_temperature, 'house_humidity': house_humidity, 'house_co2': house_co2, 'rooms': rooms_info})

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

                #get values if exists
                try:
                    room_dict['temperature'] = round(device.get_last_value().get_values().filter(value_title='temperature').first().value)
                except:
                    pass
                try:
                    room_dict['humidity'] = round(device.get_last_value().get_values().filter(value_title='humidity').first().value)
                except:
                    pass
                try:
                    room_dict['co2'] = round(device.get_last_value().get_values().filter(value_title='co2').first().value)
                except:
                    pass


            room_dict['devices'] = devices_list
            rooms_values.append(room_dict)


        return Response(rooms_values)


class ExportView(APIView):
    def get(self, request):
        devices = []

        for device in Device.objects.all():
            device_dict = {'id': device.identifier , 'name': f'{device.device_name}, {device.room.name}'}
            devices.append(device_dict)


        return Response(devices)

    def post(self, request):
        from_date = request.data['from']
        to_date = request.data['until']
        devices = request.data['devices']

        csv_data = []

        #iterate over all selected devices
        for device in devices:
            #select values by values from form
            selected_device = Device.objects.get(identifier=device['value'])
            selected_values = DeviceValuesList.objects.filter(device=selected_device, measurment_time__lte=to_date, measurment_time__gte=from_date)
            #if there is not values for device, iterator will jump to next one
            if not selected_values:
                continue

            #creating first row of csv file with titles
            value_titles = ['time']
            for titles in selected_values.first().get_values():
                value_titles.append(titles.value_title)

            #write titles into csv file
            csv_data.append(selected_device.get_values_into_csv())
            csv_data.append(value_titles)

            #write values into csv file
            for value_object in selected_values:
                #adding formated measurment_time into row
                row = [value_object.measurment_time.strftime("%Y-%m-%d %H:%M:%S")]
                #adding all values into row
                [row.append(val.value) for val in value_object.get_values()]
                #write row into csv file
                csv_data.append(row)

            #separator for better reading csv file
            csv_data.append([" "])

        return Response(csv_data)




class StatisticView(APIView):

    def get(self, request):
        
        room = Room.objects.filter(name='Chodba')[0]
        device = room.get_devices().filter(device_name="Spotřeba voda")[0]
        



        return Response({'sdf': 'sdf'})



    def post(self, request):
        pass