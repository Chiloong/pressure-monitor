import requests
from config import *

def get_wind():
    try:
        data = requests.get(OPENWEATHER_URL, params={
            "lat": LAT, "lon": LON, "appid": API_KEY, "units": "metric"
        }, timeout=10).json()

        wind = data.get("wind", {})
        speed = wind.get("speed", 0)
        deg = wind.get("deg", -1)
        gust = wind.get("gust", 0)

        trigger = (
            (speed >= WIND_SPEED_THRESHOLD or gust >= GUST_THRESHOLD)
            and (NE_MIN <= deg <= NE_MAX)
        )

        return trigger
    except:
        return False
