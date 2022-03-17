from backend.models import PullDevice, PushDevice

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

    def get_pull_devices(self):
        return PullDevice.objects.all()

    def get_push_devices(self):
        return PushDevice.objects.all()

    def get_pull_netowrk_devices(self):
        return PullDevice.objects.filter(source_type="network")