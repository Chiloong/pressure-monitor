import requests
from config import *

def get_aqi():
    try:
        data = requests.get(AQI_URL, params={
            "lat": LAT, "lon": LON, "appid": API_KEY
        }, timeout=10).json()

        level = data["list"][0]["main"]["aqi"]  # 1~5
        return level >= AQI_THRESHOLD
    except:
        return False
