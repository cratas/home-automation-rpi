import re
from sys import api_version
from textwrap import dedent
from django.shortcuts import render
from graphviz import view
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import *
from django.http import HttpResponse
from django.views import View
from django.db.models import Q
from datetime import datetime, timedelta
from collections import OrderedDict


class DeviceStatus(APIView):
    def post(self, request):
        #save incoming data into variables
        identifier = request.data['id']
        status = request.data['state']

        #find device by unique identifier and set new status
        device = Device.objects.filter(identifier=identifier)[0]
        device.is_active = status;
        device.save()

        return Response({})


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
        final_list = []

        for room in Room.objects.all():
            room_dict = {}
            room_dict['name'] = room.name

            data_dict={}

            devices_list = []
            for device in Device.objects.filter(room=room):
                device_dict = {'identifier': device.identifier, 'name' : device.device_name, 'last_time' : device.get_last_communication_time(), 'is_active' : device.is_active, 'has_error' : device.has_error }
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

                # for v in device.get_values().filter(measurment_time__gte=datetime.now()-timedelta(days=7)):
                #     try:
                #         if not v.measurment_time.strftime("%d.%m.") in data_dict.keys():
                #             data_dict[v.measurment_time.strftime("%d.%m.")].append({'co2': v.value})
                #         data_dict
                #         print(f'{v.measurment_time} -- {v.get_values().filter(value_title="co2")[0]}')
                #     except:
                #         pass


            room_dict['devices'] = devices_list
            final_list.append(room_dict)


        return Response(final_list)


class ExportView(APIView):
    def get(self, request):
        devices = []

        for device in Device.objects.all():
            if device.room is not None:
                device_dict = {'id': device.identifier , 'name': f'{device.device_name}, {device.room.name}'}
            else:
                device_dict = {'id': device.identifier , 'name': f'{device.device_name}, Celý dům'}

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
        
        test_dict = {}
        for device in Device.objects.filter(room=None):
            for values_list in device.get_values().filter(measurment_time__gte=datetime.now()-timedelta(days=30)):
                values_dict = {}

                for v in values_list.get_values().filter(Q(value_title="spotřeba") | Q(value_title="vodoměr")):
                    if not values_list.measurment_time.strftime("%d.%m.") in test_dict.keys():
                        test_dict[values_list.measurment_time.strftime("%d.%m.")] = []

                    if v.value_title == "spotřeba" and ("elektřina" in device.device_name):
                        test_dict[values_list.measurment_time.strftime("%d.%m.")].append({'elektřina': v.value})

                    if v.value_title == "vodoměr" and ("voda" in device.device_name):
                        test_dict[values_list.measurment_time.strftime("%d.%m.")].append({'voda': v.value})

                test_dict[values_list.measurment_time] = values_dict

        final_list = []

        for value in test_dict:
            if test_dict[value] is not {}:
                if len(test_dict[value]) > 0:
                    tmp = {'day': value}
                    for dict in test_dict[value]:
                        for i in dict :
                            tmp[i]=dict[i]


                    final_list.append(tmp)

        return Response(final_list)


    def post(self, request):
        pass

class TemperatureStatisticView(APIView):
    def get(self, request):
        room_name = request.GET.get('room')
        interval = int(request.GET.get('interval'))
        

        room = Room.objects.filter(name=room_name)[0]
        
        dev_list = []
        for d in Device.objects.filter(device_name__icontains="teplota", room=room):
            for value_list in d.get_values().filter(measurment_time__gte=datetime.now()-timedelta(days=interval)).order_by('measurment_time__year','measurment_time__month','measurment_time__day', 'measurment_time__minute'):
                temperature = BaseValueObject.objects.filter(value_title="temperature").filter(device_values=value_list)
                humidity = BaseValueObject.objects.filter(value_title="humidity").filter(device_values=value_list)
                values_dict = {'day': value_list.measurment_time, 'teplota' : temperature[0].value, 'vlhkost' : humidity[0].value}

                dev_list.append(values_dict)

        #remove duplicates
        seen = set()
        final_list = []
        for d in dev_list:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                final_list.append(d)


        #format date objects
        for d in final_list:
            for x in d:
                if type(d[x]) is datetime:
                    d[x] = d[x].strftime("%d.%m.")


        return Response(final_list)


class DeviceStatisticsView(APIView):
    def get(self, request):
        device_identifier = request.GET.get('device')
        interval = int(request.GET.get('interval'))

        final_list = []
        headers_list = []

        for d in Device.objects.filter(identifier=device_identifier):
            for value_list in d.get_values().filter(measurment_time__gte=datetime.now()-timedelta(days=interval)).order_by('measurment_time__year','measurment_time__month','measurment_time__day', 'measurment_time__minute'):
                values_dict = {}
                values_dict['day'] = value_list.measurment_time

                for v in BaseValueObject.objects.filter(device_values=value_list):
                    values_dict[v.value_title] = v.value 
                    headers_list.append(v.value_title)

                final_list.append(values_dict)

        #remove duplicates
        headers_list = list(dict.fromkeys(headers_list))

        #format date objects
        for d in final_list:
            for x in d:
                if type(d[x]) is datetime:
                    d[x] = d[x].strftime("%d.%m.")

        return Response({'data': final_list, 'headers': headers_list})

        