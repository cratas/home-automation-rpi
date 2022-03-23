from email.policy import default
from random import choices
from this import d
from django.db import models
from polymorphic.models import PolymorphicModel
from .helpers.parser import *
from django.utils import timezone

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

    def __str__(self):
        return f'{self.identifier}, {self.device_name}, {self.room.name}'

    def set_active(self):
        self.is_active = True

    def get_values(self):
        return DeviceValuesList.objects.filter(device=self)

    def get_last_communication_time(self):
        return DeviceValuesList.objects.filter(device=self).order_by('measurment_time').last()

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
    format = models.CharField(max_length=20, choices=FORMATS.choices, null=True)

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

