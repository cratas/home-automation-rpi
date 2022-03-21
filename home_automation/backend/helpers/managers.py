from backend.models import Device, PullDevice, PushDevice

# --------------
# SINGLETON Class for managing different types of device
# --------------
class DeviceManager:
    __instance = None

    @staticmethod
    def get_instance():
        if DeviceManager.__instance == None:
            DeviceManager()
        return DeviceManager.__instance

    def __init__(self):
        if DeviceManager.__instance != None:
            raise Exception("This class is singleton")
        else:
            DeviceManager.__instance = self

    #get device by pk
    def get_device(self, primary_key):
        return Device.objects.get(pk=primary_key)

    #simple device getters
    def get_devices(self):
        return PullDevice.objects.all()

    def get_pull_devices(self):
        return PullDevice.objects.all()

    def get_push_devices(self):
        return PushDevice.objects.all()

    #device getters by communication source
    def get_pull_network_devices(self):
        return PullDevice.objects.filter(source_type="network")

    #device getters by status 
    def get_active_pull_network_devices(self):
        return PullDevice.objects.filter(source_type="network", is_active=True)

    def get_active_push_network_devices(self):
        return PushDevice.objects.filter(is_active=True)


