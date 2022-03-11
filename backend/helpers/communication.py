from abc import ABC, abstractmethod
from pickle import NONE
import requests

#Parent class for keeping same type informations for all communication subclasses
class Communication:
    def __init__(self, source):
        self.source = source

#Derived communication abstract class for PULL method of communication
class PullCommunication(Communication, ABC):
    @abstractmethod
    def send_data_request(self):
        pass

#Derived communication abstract class for PUSH method of communication
class PushCommunication(Communication, ABC):
    #function for starting communication via request
    @abstractmethod
    def send_communication_request(self):
        pass

    #function for listening responses from server
    @abstractmethod
    def listen_data_resonses(self):
        pass

#Derived class from PullCommunication abstract class for specific communication type(network)
class NetworkPullCommunication(PullCommunication):

    def send_data_request(self):
        try:
            response = requests.get(self.source,timeout=3)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as errh:
            return("Http Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            return("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            return("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            return("OOps: Something Else",err)





