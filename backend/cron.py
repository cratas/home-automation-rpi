from .models import Test
import requests

def get_network_data():
    response = requests.get('https://pastebin.com/raw/YpAhDHBa')
    result = response.text

    Test.objects.create(name=result)