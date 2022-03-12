from multiprocessing.sharedctypes import Value
from django.contrib import admin

# from .models import Test
from .models import OneValueDevice
from .models import ValueObject

# admin.site.register(Test)
admin.site.register(OneValueDevice)
admin.site.register(ValueObject)


# Register your models here.
