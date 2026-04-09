import time
import os
import requests
from config import OPENWEATHER_URL, API_KEY, LAT, LON, PRESSURE_LOW, PRESSURE_RATE_THRESHOLD, PRESSURE_FILE

def fetch_pressure():
    try:
        resp = requests.get(f"{OPENWEATHER_URL}?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric", timeout=10)
        data = resp.json()
        pressure = data["main"]["pressure"]  # hPa
        return pressure
    except:
        return None

def read_last_pressure():
    if os.path.exists(PRESSURE_FILE):
        try:
            return float(open(PRESSURE_FILE).read().strip())
        except:
            return None
    return None

def save_pressure(p):
    with open(PRESSURE_FILE, "w") as f:
        f.write(str(p))

def get_pressure_signals():
    """
    返回:
      - low_flag: 气压低于阈值 True/False
      - drop_flag: 压力快速下降 True/False
    """
    now = time.time()
    current_pressure = fetch_pressure()
    last_pressure = read_last_pressure()

    low_flag = False
    drop_flag = False

    if current_pressure is not None:
        # ⚠️ 气压过低
        if current_pressure < PRESSURE_LOW:
            low_flag = True

        # ⚡ 压力变化率计算（hPa/小时）
        if last_pressure is not None:
            # 读取上次时间戳
            try:
                last_time = float(open(PRESSURE_FILE + ".time", "r").read().strip())
            except:
                last_time = now

            dt_hours = (now - last_time) / 3600
            rate = (last_pressure - current_pressure) / dt_hours if dt_hours > 0 else 0

            if rate > PRESSURE_RATE_THRESHOLD:
                drop_flag = True

        # 保存当前压力和时间戳
        save_pressure(current_pressure)
        with open(PRESSURE_FILE + ".time", "w") as f:
            f.write(str(now))

    return low_flag, drop_flag
