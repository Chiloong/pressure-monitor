import requests
import os
from config import OPENWEATHER_URL, LAT, LON, API_KEY, BARK_KEY, WIND_SPEED_THRESHOLD, GUST_THRESHOLD, NE_MIN, NE_MAX, WIND_STATE_FILE

def send_bark(msg):
    try:
        r = requests.get(f"{BARK_URL}/{BARK_KEY}/{msg}", timeout=10)
        print("📡 Bark状态码:", r.status_code)
    except Exception as e:
        print("❌ Bark错误:", e)

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
        wind_speed = wind.get("speed", 0)
        wind_deg = wind.get("deg", -1)
        gust = wind.get("gust", 0)
        speed_ok = wind_speed >= WIND_SPEED_THRESHOLD or gust >= GUST_THRESHOLD
        direction_ok = NE_MIN <= wind_deg <= NE_MAX
        current_state = "ON" if (speed_ok and direction_ok) else "OFF"
        last_state = load_last_state()
        if last_state == "OFF" and current_state == "ON":
            send_bark(f"🏭东北风触发\n风速:{wind_speed}m/s\n阵风:{gust}m/s\n风向:{wind_deg}°")
        save_state(current_state)
        print(f"🌬 风速:{wind_speed}m/s 风向:{wind_deg}° 阵风:{gust}m/s 状态:{current_state}")
        return wind_speed, wind_deg
    except Exception as e:
        print("❌ Wind Error:", e)
        return None, None
