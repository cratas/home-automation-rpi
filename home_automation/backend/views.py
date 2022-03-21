from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from abc import abstractstaticmethod
from django.http import HttpResponse, Http404
from django.views import View
import requests

from .forms import PullDeviceForm, PushDeviceForm, ExportForm, RoomForm

from .helpers.parser import *
from .helpers.managers import DeviceManager
from .models import *

#view function returning all rooms in house
def home(request):
    rooms = Room.objects.all()
    return render(request, 'index.html', {'rooms':rooms})

#view function for creating new room
def rooms(request):
    room_form = RoomForm(request.POST or None)

    if room_form.is_valid():
        room_form.save()
        return redirect('rooms') 

    return render(request, 'rooms.html', {'room_form':room_form})


def add_device(request, device_type):

    if device_type == 'pull':
        device_form = PullDeviceForm(request.POST or None)
    else:
        device_form = PushDeviceForm(request.POST or None)

    if device_form.is_valid():
        device_form.save()
        return redirect('home')

    return render(request, 'devices.html', {'device_form':device_form, 'device_type': device_type})
    


#view function for updating devices
def update_device(request, device_id, device_type):
    device = Device.objects.get(pk=device_id)

    if device_type == 'pull':
        device_form = PullDeviceForm(request.POST or None, instance=device)
    else:
        device_form = PushDeviceForm(request.POST or None, instance=device)

    if device_form.is_valid():
        device_form.save()
        return redirect('home')

    return render(request, 'devicesupdate.html', {'device_form':device_form, 'device':device})


class Export(View):
    def get(self, request):
        export_form = ExportForm()
        return render(request, 'export.html', {'export_form':export_form})

    def post(self, request):
        export_form = ExportForm(request.POST)
        if export_form.is_valid():
            #getting values from form
            from_date = export_form.cleaned_data['from_date']
            to_date = export_form.cleaned_data['to_date']
            device = export_form.cleaned_data['device']

            #select values by values from form
            selected_device = Device.objects.get(pk=device)
            selected_values = DeviceValuesList.objects.filter(device=selected_device, measurment_time__lte=to_date, measurment_time__gte=from_date)

            if not selected_values:
                export_form = ExportForm()
                return render(request, 'export.html', {'no_data_warning': '1', 'export_form':export_form})

            #creating first row of csv file with titles
            value_titles = ['time']
            for titles in selected_values.first().get_values():
                value_titles.append(titles.value_title)

            #creating and setting response
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=data.csv'

            #creating csv writer
            writer = csv.writer(response)
            #write titles into csv file
            writer.writerow(value_titles)

            #write values into csv file
            for value_object in selected_values:
                #adding formated measurment_time into row
                row = [value_object.measurment_time.strftime("%Y-%m-%d %H:%M:%S")]
                #adding all values into row
                [row.append(val.value) for val in value_object.get_values()]
                #write row into csv file
                writer.writerow(row)

            return response


            # export_form = ExportForm()
        # return render(request, 'export.html', {'export_form':export_form})

        

# ----------------------------------------------------------------------
# COMMUNICATION SOLUTIONS
# ----------------------------------------------------------------------
def testing_function(request):


    # print(DeviceManager.get_instance().get_active_pull_netowrk_devices())
    NetworkPullCommunication.process_data()

    return HttpResponse("sdfsdf")

# --------------
# PULL COMMUNICATION CLASSES
# --------------
class PullCommunication(ABC):
    
    @abstractstaticmethod
    def get_data():
        pass

    @abstractstaticmethod
    def process_data():
        pass

class NetworkPullCommunication(PullCommunication):
    
    def get_data(source_address):
        try:
            response = requests.get(source_address,timeout=3)
            response.raise_for_status()

            return response.text
        except:
            return None

    def process_data():

        for device in DeviceManager.get_instance().get_active_pull_network_devices():
            retrieved_data = NetworkPullCommunication.get_data(device.source_address)

            if retrieved_data is None:
                print(f'Cannot retreive {device.device_name}:{device.identifier} data from {device.source_address}')
                continue

            parser = ParserFactory.get_instance().create_parser(device.format, retrieved_data, ',')
            parser.parse_into_dict()

             #iterate over all dicts in dict list
            for dict_object in parser.data:
                values_list = DeviceValuesList.objects.create(device=device)

                #iterate over every dict inside list
                for key, value in dict_object.items():
                    if key == 'id':
                        continue
                    #convert to correct float format
                    if "," in value:
                        value = value.replace(',','.')
        
                    #creating correct type of value
                    if is_number(value):
                        NumericValueObject.objects.create(value_title=key, value=value, device_values=values_list)
                    else:
                        StringValueObject.objects.create(value_title=key, value=value, device_values=values_list)


class SerialBusPullCommunication(PullCommunication):
    
    def get_data():
        pass

    def process_data(self):
        pass

# --------------
# PUSH COMMUNICATION CLASSES
# --------------
class PushCommunication():
    def __init__(self):
        self.parser_type='parametres'
        self.retreived_data = None

    def process_data(self):

        #getting device id from incoming data
        device_identifier = self.retreived_data[0]["id"]

        #if device with incoming id does not exist, method will return False
        try:
            device = DeviceManager.get_instance().get_active_push_network_devices().get(identifier=device_identifier)
        except ObjectDoesNotExist:
            return False

        #iterate over all dicts in dict list
        for dict_object in self.retreived_data:
            values_list = DeviceValuesList.objects.create(device=device)

            #iterate over every dict inside list
            for key, value in dict_object.items():
                #ignore values with key id
                if key == 'id':
                    continue

                #convert to correct float format
                if "," in value:
                    value = value.replace(',','.')
    
                #creating correct type of value
                if is_number(value):
                    NumericValueObject.objects.create(value_title=key, value=value, device_values=values_list)
                else:
                    StringValueObject.objects.create(value_title=key, value=value, device_values=values_list)
 
        return True

class NetworkPushCommunication(PushCommunication, View):
    def get(self, request):
        #getting data via get request
        incoming_data = request.GET

        #checking if incoming data aren't null
        if not incoming_data:
            return HttpResponse("Data NOT inserted into database")
 
        #retrieved data are already represented as dic
        parser = ParserFactory.get_instance().create_parser(self.parser_type, incoming_data, ',')
        parser.parse_into_dict()

        self.retreived_data = parser.data

        #process data
        if self.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")

        return HttpResponse("Data NOT inserted into database")
 
    def post(self, request, *args, **kwargs):
        #specific format of incoming data
        self.parser_type = kwargs['name']
        #getting data via post request
        incoming_data = request.body.decode('utf-8')
 
        #checking if incoming data aren't null
        if not incoming_data:
            return HttpResponse("Data NOT inserted into database")
 
        #parsing retrieved data via parser
        parser = ParserFactory.get_instance().create_parser(self.parser_type, incoming_data, ',')
        parser.parse_into_dict()
 
        self.retreived_data = parser.data

        #process data
        if self.process_data() is True:
            return HttpResponse("Data inserted into database")
        else:
            return HttpResponse("Data NOT inserted into database")

        return HttpResponse("Data NOT inserted into database")


class SerialBusPushCommunication(PushCommunication):

    def __init__(self, trans_speed, trans_size, stop_bit):
        self.parser_type='csv'
        self.trans_speed = trans_speed
        self.trans_size = trans_size
        self.stop_bit = stop_bit

    def get_data(self):
        pass
