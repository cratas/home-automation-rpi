# #ENABLE crontab function: python manage.py crontab add
# #DISABLE crontab function: python manage.py crontab remove

from .views import NetworkPullCommunication, push_check
from .helpers.managers import DeviceManager
from datetime import datetime, timezone
from django.core.mail import send_mail


def get_network_data():
    NetworkPullCommunication.process_data()
    push_check()

#     for device in DeviceManager.get_instance().get_active_push_network_devices():
#         #increment counter
#         device.communication_counter = device.communication_counter + 1
#         device.save()


#         if device.communication_counter == device.communication_interval * 3:
#             #reset counter back to 0
#             device.communication_counter = 0
#             device.save()

#             #getting last communication time from current device
#             last_communication_time = device.get_last_communication_time() 

#             #if there are no measured data, time diff will be None value for check below
#             if last_communication_time is None:
#                 diff_in_minutes = None
#             else:
#                 #count diff in minutes between timestamp and last communication
#                 diff_in_minutes = (datetime.now(timezone.utc) - last_communication_time).total_seconds() / 60.0

#             #if the time difference is greater than 3 intervals (no data from device for 3 times) or there are not incoming values at all, set device error
#             if diff_in_minutes > device.communication_interval * 3 or diff_in_minutes is None:
#                 device.has_error=True
#                 device.is_active=False
#                 device.save()
                
#                 send_mail(
#                         'Device error',
#                         f'Communication with id: {device.identifier} failed.',
#                         'from@example.com', 
#                         ['to@example.com'], #list of users
#                         fail_silently=False,
#                     )
                
#                 print(f'No data from {device.device_name}:{device.identifier} for the third time.')



