import requests, time, json
from config import *

def read_cache():
    try:
        return json.load(open(CACHE_FILE))
    except:
        return {"t": 0}

def save_cache(data):
    json.dump(data, open(CACHE_FILE, "w"))

def get_all():
    cache = read_cache()
    now = time.time()

    # ✅ 60秒缓存（防止重复调用）
    if now - cache.get("t", 0) < 60:
        return cache["data"]

    params = {
        "location": f"{LON},{LAT}",
        "key": QWEATHER_API_KEY
    }

    w = requests.get(QWEATHER_NOW, params=params, timeout=10).json()["now"]
    a = requests.get(QWEATHER_AIR, params=params, timeout=10).json()["now"]

    data = {
        "pressure": float(w["pressure"]),
        "humidity": float(w["humidity"]),
        "wind_speed": float(w["windSpeed"]),
        "wind_dir": float(w["wind360"]),
        "aqi": int(a["aqi"])
    }

    save_cache({"t": now, "data": data})
    return data
