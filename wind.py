import requests
import os
from config import OPENWEATHER_URL, LAT, LON, API_KEY, BARK_KEY, WIND_SPEED_THRESHOLD, GUST_THRESHOLD, NE_MIN, NE_MAX, WIND_STATE_FILE

def send_bark(msg):
    try:
        requests.get(f"https://api.day.app/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

def load_last_state():
    if os.path.exists(WIND_STATE_FILE):
        with open(WIND_STATE_FILE, "r") as f:
            return f.read().strip()
    return "OFF"

def save_state(state):
    with open(WIND_STATE_FILE, "w") as f:
        f.write(state)

def check_wind():
    try:
        params = {"lat": LAT, "lon": LON, "appid": API_KEY, "units": "metric"}
        data = requests.get(OPENWEATHER_URL, params=params, timeout=10).json()

        wind = data.get("wind", {})
        speed = wind.get("speed", 0)
        deg = wind.get("deg", -1)
        gust = wind.get("gust", 0)

        speed_ok = speed >= WIND_SPEED_THRESHOLD or gust >= GUST_THRESHOLD
        direction_ok = NE_MIN <= deg <= NE_MAX

        state = "ON" if (speed_ok and direction_ok) else "OFF"
        last = load_last_state()

        if last == "OFF" and state == "ON":
            send_bark(f"🏭东北风触发 风速:{speed} 风向:{deg}")

        save_state(state)

        print(f"🌬 风:{speed}m/s 方向:{deg}")

        return speed, deg

    except Exception as e:
        print("❌ Wind Error:", e)
        return 0, -1
