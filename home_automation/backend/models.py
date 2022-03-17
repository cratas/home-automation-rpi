from random import choices
from django.db import models
from polymorphic.models import PolymorphicModel





# ----------
# ROOM MODEL
# ----------
class Room(models.Model):
    name = models.CharField(max_length=10)

# ----------
# DEVICE MODEL
# ----------
class Device(PolymorphicModel):
    identifier = models.CharField(max_length=20, unique=True)
    device_name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f'{self.identifier}'


class PushDevice(Device):
    def __str__(self):
        return f'Push device:{self.identifier}'

class PullDevice(Device):
    source_address = models.CharField(max_length=50, unique=True, null=True)
    class FORMATS(models.TextChoices):
        CSV = 'csv'
        PARAMETRES = 'parametres'
    format = models.CharField(max_length=20, choices=FORMATS.choices, null=True)

    def __str__(self):
        return f'Pull device:{self.identifier}, {self.source_address}, {self.format}'

    def get_new_data(self):
    #TODO - create communication class
        pass
# ----------    
# DEVICE VALUES LIST MODEL
# ----------
class DeviceValuesList(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

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

