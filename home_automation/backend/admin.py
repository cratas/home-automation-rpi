from .models import PullDevice, PushDevice, Room, Device, DeviceValuesList, SmartDevice, StringValueObject, NumericValueObject, BooleanValueObject
from django.contrib import admin

# register my modules into admin site
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(PushDevice)
admin.site.register(PullDevice)
admin.site.register(DeviceValuesList)
admin.site.register(StringValueObject)
admin.site.register(NumericValueObject)
admin.site.register(BooleanValueObject)
admin.site.register(SmartDevice)
