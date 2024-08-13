import requests
import ssl
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

class SSLAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)

def get_balance(api_key):
    url = f"https://2captcha.com/res.php?key={api_key}&action=getbalance"
    session = requests.Session()
    session.mount('https://', SSLAdapter())
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

api_key = "2b8c9292ea263ff1479ca8fef38f9d6f"
balance = get_balance(api_key)
if balance:
    print(f"Your balance is: {balance}")
else:
    print("Failed to retrieve balance.")