# #ENABLE crontab function: python manage.py crontab add
# #DISABLE crontab function: python manage.py crontab remove

from .views import NetworkPullCommunication

def get_network_data():
    NetworkPullCommunication.process_data()


