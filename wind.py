import requests
import os

LAT = 35.21
LON = 113.29

API_KEY = os.environ["API_KEY"]
BARK_KEY = os.environ["BARK_KEY"]

WIND_SPEED_THRESHOLD = 2.5
GUST_THRESHOLD = 4.0
NE_MIN = 20
NE_MAX = 100

STATE_FILE = "state/wind.txt"


def send_bark(msg):
    requests.get(f"https://api.day.app/{BARK_KEY}/{msg}", timeout=10)


def load_last_state():
    try:
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    except:
        return "OFF"


def save_state(state):
    os.makedirs("state", exist_ok=True)
    with open(STATE_FILE, "w") as f:
        f.write(state)


def check_wind():
    try:
        url = (
            f"https://api.openweathermap.org/data/2.5/weather?"
            f"lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        )

        data = requests.get(url, timeout=10).json()

        wind = data.get("wind", {})
        wind_speed = wind.get("speed", 0)
        wind_deg = wind.get("deg", -1)
        gust = wind.get("gust", 0)

        speed_ok = wind_speed >= WIND_SPEED_THRESHOLD or gust >= GUST_THRESHOLD
        direction_ok = NE_MIN <= wind_deg <= NE_MAX

        current_state = "ON" if (speed_ok and direction_ok) else "OFF"
        last_state = load_last_state()

        if last_state == "OFF" and current_state == "ON":
            send_bark(
                f"🏭东北风触发\n"
                f"风速:{wind_speed}m/s\n"
                f"阵风:{gust}m/s\n"
                f"风向:{wind_deg}°"
            )

        save_state(current_state)

    except Exception as e:
        print("Wind Error:", e)
