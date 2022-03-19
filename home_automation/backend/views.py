from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from abc import abstractstaticmethod
from django.http import HttpResponse, Http404
from django.views import View
import requests

from .helpers.parser import *
from .helpers.managers import DeviceManager
from .models import *



def home(request):

    rooms = Room.objects.all()
    return render(request, 'index.html', {'rooms':rooms})

def rooms(request):
    # if request.user.groups.filter(name = "Staff").exists():
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {'rooms':rooms})

    # raise Http404()

def devices(request):
    return render(request, 'devices.html',{
        'push_devices': DeviceManager.get_instance().get_push_devices(),
        'pull_devices': DeviceManager.get_instance().get_pull_devices()
    })


def export(request):
    return render(request, 'export.html', {})
# ----------------------------------------------------------------------
# COMMUNICATION SOLUTIONS
# ----------------------------------------------------------------------
def testing_function(request):

    # communication = NetworkPullCommunication()
    # communication.process_data()
    # print(DeviceManager.get_instance().get_pull_netowrk_devices())
    # NetworkPullCommunication.process_data()

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

        for device in DeviceManager.get_instance().get_pull_devices():
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
            device = PushDevice.objects.get(identifier=device_identifier)
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
