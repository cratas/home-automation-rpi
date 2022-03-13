from django.contrib import admin

# from .models import Test
# from .models import OneValueDevice
from .models import TestingValueObject, TestingDevice



# Register your models here.

# admin.site.register(Test)
# admin.site.register(OneValueDevice)
admin.site.register(TestingDevice)
admin.site.register(TestingValueObject)


