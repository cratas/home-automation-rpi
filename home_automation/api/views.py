from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import *
from django.db.models import Q
from datetime import datetime, timedelta

# APIView class for returning status of device specified via POST request parametres
class DeviceStatus(APIView):
    def post(self, request):
        #save incoming data into variables
        identifier = request.data['id']
        status = request.data['state']
        is_smart_device = request.data['isSmartDevice']

        #find device by type and unique identifier and set new status
        if is_smart_device:
            device = SmartDevice.objects.filter(identifier=identifier)[0]
        else:
            device = Device.objects.filter(identifier=identifier)[0]

        device.is_active = status;
        device.save()

        return Response({})

# APIView class for returning data into main frontend dashboard
# data contains avg house temperature, humidity and CO2
class DashboardView(APIView):
    def get(self, request):

        # counting avg values for whole house
        house_temperature = Device.count_avg('temperature')
        house_humidity = Device.count_avg('humidity')
        house_co2 = Device.count_avg('co2')

        rooms_info = []

        # filling list of room dicts with number of devices by type
        for room in Room.objects.all():
            room = {
                'name': room.name,
                'active_count': room.get_active_dev_count(),
                'non_active_count': room.get_non_active_dev_count(),
                'error_count': room.any_device_has_error()
            }
            rooms_info.append(room)

        return Response({'house_temperature': house_temperature, 'house_humidity': house_humidity, 'house_co2': house_co2, 'rooms': rooms_info})


# APIView class for returning tempr, humidity, co2 and devices for every room
class RoomsView(APIView):
    def get(self, request):
        final_list = []

        # iterate over all rooms in house
        for room in Room.objects.all():
            room_dict = {}
            room_dict['name'] = room.name

            # iterate over all devices in room
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

            smart_devices_list = []

            # iterate over all smart devices like lights, fans and heating and add them into smart_devices list
            for smart_device in SmartDevice.objects.filter(room=room):
                smart_device_dict = {'identifier': smart_device.identifier, 'name' : smart_device.device_name, 'is_active': smart_device.is_active, 'type' : smart_device.type }
                smart_devices_list.append(smart_device_dict)

            # add current device or smart device into final list
            room_dict['devices'] = devices_list
            room_dict['smart_devices'] = smart_devices_list
            final_list.append(room_dict)

        return Response(final_list)

# APIView class for returning data to form and handling post request
class ExportView(APIView):
    # function executed by get request, send all devices in house via response
    def get(self, request):
        devices = []

        # iterate over all devices in room
        for device in Device.objects.all():
            if device.room is not None:
                device_dict = {'id': device.identifier , 'name': f'{device.device_name}, {device.room.name}'}
            else:
                device_dict = {'id': device.identifier , 'name': f'{device.device_name}, Celý dům'}

            devices.append(device_dict)

        return Response(devices)

    # function executed by post request, returning data in csv format for devices specified in parametres of request
    def post(self, request):
        from_date = request.data['from']
        to_date = request.data['until']
        devices = request.data['devices']

        csv_data = []

        # iterate over all selected devices
        for device in devices:
            # select values by values from form
            selected_device = Device.objects.get(identifier=device['value'])
            selected_values = DeviceValuesList.objects.filter(device=selected_device, measurment_time__lte=to_date, measurment_time__gte=from_date)
            # if there is not values for device, iterator will jump to next one
            if not selected_values:
                continue

            # creating first row of csv file with titles
            value_titles = ['time']
            for titles in selected_values.first().get_values():
                value_titles.append(titles.value_title)

            # write titles into csv file
            csv_data.append(selected_device.get_values_into_csv())
            csv_data.append(value_titles)

            # write values into csv file
            for value_object in selected_values:
                # adding formated measurment_time into row
                row = [value_object.measurment_time.strftime("%Y-%m-%d %H:%M:%S")]
                # adding all values into row
                [row.append(val.value) for val in value_object.get_values()]
                # write row into csv file
                csv_data.append(row)

            # adding separator between device values
            csv_data.append([" "])

        return Response(csv_data)

# APIView class for returning house consumption data
class StatisticView(APIView):
    def get(self, request):
        
        test_dict = {}
        # iterate over all devices which are set for measuring data in whole house
        for device in Device.objects.filter(room=None):
            # iterate over all values lists in measured last month
            for values_list in device.get_values().filter(measurment_time__gte=datetime.now()-timedelta(days=30)):
                values_dict = {}

                # iterate over all values in current values list
                for v in values_list.get_values().filter(Q(value_title="spotřeba") | Q(value_title="vodoměr")):
                    if not values_list.measurment_time.strftime("%d.%m.") in test_dict.keys():
                        test_dict[values_list.measurment_time.strftime("%d.%m.")] = []

                    if v.value_title == "spotřeba" and ("elektřina" in device.device_name):
                        test_dict[values_list.measurment_time.strftime("%d.%m.")].append({'elektřina': v.value})

                    if v.value_title == "vodoměr" and ("voda" in device.device_name):
                        test_dict[values_list.measurment_time.strftime("%d.%m.")].append({'voda': v.value})

                test_dict[values_list.measurment_time] = values_dict

        final_list = []

        # format data into format required by recharts library on frontend: [{key: val, key: val}]
        for value in test_dict:
            if test_dict[value] is not {}:
                if len(test_dict[value]) > 0:
                    tmp = {'day': value}
                    for dict in test_dict[value]:
                        for i in dict :
                            tmp[i]=dict[i]

                    final_list.append(tmp)

        return Response(final_list)

# APIView class for returning temperature and humidity data for specific room in specific interval
class TemperatureStatisticView(APIView):
    def get(self, request):
        # getting data from parameters
        room_name = request.GET.get('room')
        interval = int(request.GET.get('interval'))

        # get room object by name in request parameter
        room = Room.objects.filter(name=room_name)[0]
        
        dev_list = []
        # iterate over all devices which measure temperature and humidity in specific room
        for d in Device.objects.filter(device_name__icontains="teplota", room=room):
            # iterate over all values measured in specific interval ordered by time
            for value_list in d.get_values().filter(measurment_time__gte=datetime.now()-timedelta(days=interval)).order_by('measurment_time__year','measurment_time__month','measurment_time__day', 'measurment_time__minute'):
                temperature = BaseValueObject.objects.filter(value_title="temperature").filter(device_values=value_list)
                humidity = BaseValueObject.objects.filter(value_title="humidity").filter(device_values=value_list)
                values_dict = {'day': value_list.measurment_time, 'teplota' : temperature[0].value, 'vlhkost' : humidity[0].value}

                dev_list.append(values_dict)

        # remove duplicates
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

# APIView class for returning all measured values for specific device in specific interval
class DeviceStatisticsView(APIView):
    def get(self, request):
        # getting data from parameters
        device_identifier = request.GET.get('device')
        interval = int(request.GET.get('interval'))

        final_list = []
        headers_list = []

        # getting all measured values for specific device/s in specific interval ordered by time
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

        
