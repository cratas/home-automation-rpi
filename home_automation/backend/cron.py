
from .views import NetworkPullCommunication
from .helpers.managers import DeviceManager
from datetime import datetime, timezone

# ENABLE crontab function: python manage.py crontab add
# DISABLE crontab function: python manage.py crontab remove

# crontab function which is executed periodically by interval set in setting.py file
def communicate():
    #iterate over all active pull devices and ask for data
    NetworkPullCommunication.process_data()
 
    # iterate over all active push devices
    for device in DeviceManager.get_instance().get_active_push_network_devices():
            #increment communication counter
            device.communication_counter = device.communication_counter + 1
            device.save()

            # if communication counter is equal to interval * 3, device responses the time
            # since the last communication with the device will be checked
            if device.communication_counter == device.communication_interval * 3:
                # reset counter back to 0
                device.communication_counter = 0
                device.save()

                # getting last communication time from current device
                last_communication_time = device.get_last_communication_time() 

                # if there are no measured data, time diff will be None value for check below
                if last_communication_time is None:
                    diff_in_minutes = None
                else:
                    # count diff in minutes between timestamp and last communication
                    diff_in_minutes = (datetime.now(timezone.utc) - last_communication_time).total_seconds() / 60.0

                # if the time difference is greater than 3 intervals (no data from device for 3 times) or
                # there are not incoming values at all, set device error
                if diff_in_minutes > device.communication_interval * 3 or diff_in_minutes is None:
                    # print("ZARIZENI NEODPOVIDA")
                    device.handle_error()


