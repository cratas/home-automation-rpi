from argparse import ONE_OR_MORE
from tkinter import CASCADE
from django.db import models
import abc
from .helpers.communication import *
from .helpers.parser import *
#Just testing model, gonna be removed
# class Test(models.Model):
#     name = models.CharField(max_length=4)



class TestingDevice(models.Model):
    identifier = models.CharField(max_length=20, unique=True)

class TestingValueObject(models.Model):
    value_name = models.CharField(max_length=20)
    value = models.CharField(max_length=20)
    device = models.ForeignKey(TestingDevice, on_delete=models.CASCADE)


# class OneValueDevice(models.Model):
#     device_name = models.CharField(max_length=10)

#     def __str__(self):
#         return f"{self.device_name}"


#     def add_measured_value(self):
#         communication = NetworkPullCommunication("https://pastebin.com/raw/Az8Jr8GC")
#         incoming_data = communication.send_data_request()
#         parser = ParserCSV(incoming_data)
#         parsed_values = {}
#         parsed_values = parser.get_parsed_data()

#         #create new measuredValue object and add to current DeviceObject
#         temp_sensor = OneValueDevice.objects.get(device_name=self.device_name)

#         for k, v in temp_sensor.items():
#             ValueObject.objects.create(value_name=parsed_values[k], value=v, device=temp_sensor)



        


# class ValueObject(models.Model):
#     value_name = models.CharField(max_length=10)
#     value = models.CharField(max_length=20)
#     device = models.ForeignKey(OneValueDevice, on_delete=models.CASCADE)

#     def __str__(self):
#         return f"{self.value_name} : {self.value}"

# #Room model with his name and N sensors inside
# class Room(models.Model):
#     name = models.CharField(max_length=10)


# # ----------
# # DEVICE MODELS
# # ----------
# class AbstractDeviceMeta(abc.ABCMeta, type(models.Model)):
#     pass

# #ABSTRACT Device model(Sensor) with his name and specific room
# class AbstractDevice(models.Model, metaclass=AbstractDeviceMeta):    
#     name = models.CharField(max_length=10)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)

#     class Meta:
#         abstract = True

#     @abc.abstractmethod
#     def get_new_data(self):
#         pass


# class ManyValueDevice(AbstractDevice):
#     def get_new_data(self):
#         communication = NetworkPullCommunication("https://pastebin.com/raw/Az8Jr8GC")
#         #create new measuredValue object and add to current DeviceObject
#         self.name = communication.send_data_request()


# class MeasuredValues(models.Model):
#     device = models.ForeignKey(AbstractDevice, on_delete=models.CASCADE)

# # ----------
# # VALUES MODELS
# # ----------
# class AbstractValue(models.Model):
#     name = models.CharField(max_length=10)
#     measured_values = models.ForeignKey(MeasuredValues, on_delete=models.CASCADE);

#     class Meta:
#         abstract = True

# class StringValue(AbstractValue):
#     value = models.CharField(max_length=20)

# class BooleanValue(AbstractValue):
#     value = models.BooleanField()

# class DecimalValue(AbstractValue):
#     value = models.DecimalField(max_digits=10, decimal_places=3)







