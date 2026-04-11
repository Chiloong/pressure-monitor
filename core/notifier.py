import requests
from config import BARK_KEY


def send(msg):
    print("bark send")
    url = f"https://api.day.app/{BARK_KEY}/{msg}"
    try:
        r = requests.get(url, timeout=10)
        print(r.status_code)
    except:
        print("bark error")
