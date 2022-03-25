from django.db import models
from polymorphic.models import PolymorphicModel
from .helpers.parser import *
from django.utils import timezone
from django.core.mail import send_mail
from datetime import datetime


# ----------
# ROOM MODEL
# ----------
class Room(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}'

    def get_dev_count(self):
        return Device.objects.filter(room=self).count()

    def get_active_dev_count(self):
        return Device.objects.filter(room=self, is_active=True).count()

    def get_non_active_dev_count(self):
        return Device.objects.filter(room=self, is_active=False).count()

    def get_devices(self):
        return Device.objects.filter(room=self)
# ----------
# DEVICE MODEL
# ----------
def default_set():
    return Room.objects.get(name='Kuchyně').id

class Device(PolymorphicModel):
    identifier = models.CharField(max_length=20, unique=True)
    device_name = models.CharField(max_length=30, null=True)
    is_active = models.BooleanField(default=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    error_count = models.IntegerField(default=0)
    has_error = models.BooleanField(default=False)
    communication_interval = models.IntegerField(default=1) #one interval unit is 1 minute
    communication_counter = models.IntegerField(default=0)
    datetime_title = models.CharField(max_length=30, null=True)
    date_title = models.CharField(max_length=20, null=True)
    time_title = models.CharField(max_length=20, null=True)
    datetime_format = models.CharField(max_length=30, default="%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f'{self.identifier}, {self.device_name}, {self.room.name}'

    def set_active(self):
        self.is_active = True

    def get_values(self):
        return DeviceValuesList.objects.filter(device=self)

    def get_last_communication_time(self):
        #getting count of values for condition below
        values_count = DeviceValuesList.objects.filter(device=self).order_by('measurment_time').count()

        #if there is no data None will be returned
        if values_count > 0:
            return DeviceValuesList.objects.filter(device=self).order_by('measurment_time').last().measurment_time
        return None
        
    def get_values_into_csv(self):
        return [f'{self.identifier} {self.device_name} {self.room}']

    def handle_error(self):
        self.has_error=True
        self.is_active=False
        self.error_count=0
        self.save()
                #sending email to user, contact informations has to be set
        send_mail(
            'Device error',
            f'Communication with id: {self.identifier} failed.',
            'from@example.com', 
            ['to@example.com'], #list of users
            fail_silently=False,
        )

    def save_data(self, data):
        #iterate over all dicts in dict list
        for dict_object in data:
            values_list = DeviceValuesList.objects.create(device=self)

            #variable for creating datetime from two columns
            datetime_str = ""

            #iterate over every dict inside list
            for key, value in dict_object.items():
                #ignore values with key id
                if key == 'id':
                    continue
                
                #checking if mesurment time is part of data, if no, default time is set to timestamp
                if self.datetime_title is not None:
                    if key == self.datetime_title:
                        datetime_str = value
                        datetime_object = self.strptime(datetime_str, self.datetime_format)
                        values_list.measurment_time = datetime_object
                        values_list.save()
                        continue

                if self.date_title is not None and self.time_title is not None:
                    if key == self.date_title:
                        datetime_str = value
                        continue
                    
                    if key == self.time_title:
                        datetime_str = datetime_str + ' ' + value
                        datetime_object = datetime.strptime(datetime_str, self.datetime_format)
                        values_list.measurment_time = datetime_object
                        values_list.save()
                        continue

                #convert to correct float format
                if "," in value:
                    value = value.replace(',','.')
    
                #creating correct type of value
                if is_number(value):
                    NumericValueObject.objects.create(value_title=key, value=value, device_values=values_list)
                else:
                    StringValueObject.objects.create(value_title=key, value=value, device_values=values_list)

class PushDevice(Device):
    pass

class PullDevice(Device):
    source_address = models.CharField(max_length=50, unique=True, null=True)
    class CHANNELS(models.TextChoices):
        NETWORK = 'network'
        SERIALBUS = 'serial_bus'
    source_type = models.CharField(max_length=20, choices=CHANNELS.choices, default=CHANNELS.NETWORK)
    
    class FORMATS(models.TextChoices):
        CSV = 'csv'
        PARAMETRES = 'parametres'
    format = models.CharField(max_length=20, choices=FORMATS.choices, default=FORMATS.choices[0])
    delimiter = models.CharField(max_length=1, default=',')

# ----------    
# DEVICE VALUES LIST MODEL
# ----------
class DeviceValuesList(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    measurment_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        values = BaseValueObject.objects.filter(device_values=self)
        values_string = ''

        for value_object in values:
            values_string+= f'{value_object.value_title}:{value_object.value} | '
        return f'{self.measurment_time} | {values_string}'

    def get_values(self):
        return BaseValueObject.objects.filter(device_values=self)

# ----------
# VALUE OBJECT MODEL
# ----------
class BaseValueObject(PolymorphicModel):
    value_title = models.CharField(max_length=30)
    device_values = models.ForeignKey(DeviceValuesList, on_delete=models.CASCADE)

class StringValueObject(BaseValueObject):
    value = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.value_title}:{self.value}'

class NumericValueObject(BaseValueObject):
    value = models.DecimalField(max_digits=10, decimal_places=3)

    def __str__(self):
        return f'{self.value_title}:{self.value}'

class BooleanValueObject(BaseValueObject):
    value = models.BooleanField()

    def __str__(self):
        return f'{self.value_title}:{self.value}'

