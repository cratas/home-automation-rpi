# from .models import OneValueDevice, ValueObject


# #ENABLE crontab function: python manage.py crontab add
# #DISABLE crontab function: python manage.py crontab remove


from .views import NetworkPullCommunication


def get_network_data():
    
    NetworkPullCommunication.process_data()

    # temp_sensor = OneValueDevice.objects.get(device_name="tempSensor")
    # ValueObject.objects.create(value_name="tempr", value="42", device=temp_sensor)
    # devices = []
    # for device in devices:
    #     device.get_new_data()
