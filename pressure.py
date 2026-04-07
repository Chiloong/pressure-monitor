import requests
import time
from config import OPENWEATHER_URL, LAT, LON, API_KEY, BARK_KEY, PRESSURE_STATE_FILE, PRESSURE_RATE_THRESHOLD

def send_bark(msg):
    try:
        url = f"https://api.day.app/{BARK_KEY}/{msg}"
        r = requests.get(url, timeout=10)
        print("📡 Bark:", r.status_code)
    except Exception as e:
        print("❌ Bark错误:", e)

def get_pressure():
    params = {"lat": LAT, "lon": LON, "appid": API_KEY, "units": "metric"}
    data = requests.get(OPENWEATHER_URL, params=params, timeout=10).json()
    return data["main"]["pressure"]

def read_history():
    try:
        with open(PRESSURE_STATE_FILE, "r") as f:
            lines = f.readlines()
            return [tuple(map(float, line.strip().split(","))) for line in lines]
    except:
        return []

def save_history(p, t):
    history = read_history()
    history.append((p, t))
    history = history[-3:]
    with open(PRESSURE_STATE_FILE, "w") as f:
        for p, t in history:
            f.write(f"{p},{t}\n")

def check_pressure():
    print("🔥 气压模块运行")

    try:
        current_p = get_pressure()
        current_t = time.time()

        history = read_history()

        rate = 0
        accel = 0

        if len(history) >= 2:
            p1, t1 = history[-2]
            p2, t2 = history[-1]

            rate1 = (p2 - p1) / ((t2 - t1) / 3600)
            rate2 = (current_p - p2) / ((current_t - t2) / 3600)

            rate = rate2
            accel = rate2 - rate1

            print(f"📈 速率: {rate:.2f} hPa/h")
            print(f"⚡ 加速度: {accel:.2f}")

            if abs(rate) > PRESSURE_RATE_THRESHOLD:
                direction = "📉下降" if rate < 0 else "📈上升"
                send_bark(f"🌡气压异常 {direction} {rate:.2f}")

        else:
            print("⚠️ 数据不足")

        save_history(current_p, current_t)

        return rate, accel

    except Exception as e:
        print("❌ Pressure Error:", e)
        return 0, 0
