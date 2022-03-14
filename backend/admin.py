from django.contrib import admin

from .models import Room, Device, DeviceValuesList, BaseValueObject, StringValueObject, NumericValueObject, BooleanValueObject

#register my modules
admin.site.register(Room)
admin.site.register(Device)
admin.site.register(DeviceValuesList)
admin.site.register(StringValueObject)
admin.site.register(NumericValueObject)
admin.site.register(BooleanValueObject)




