import requests
import os
import time

LAT = 35.21
LON = 113.29

API_KEY = os.environ["API_KEY"]
BARK_KEY = os.environ["BARK_KEY"]

STATE_FILE = "pressure_state.txt"


def send_bark(msg):
    try:
        url = f"https://api.day.app/{BARK_KEY}/{msg}"
        print("🚀 Bark:", msg)
        r = requests.get(url, timeout=10)
        print("📡 状态码:", r.status_code)
    except Exception as e:
        print("❌ Bark错误:", e)


def get_pressure():
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
    )
    print("🌍 请求天气数据...")
    data = requests.get(url, timeout=10).json()
    return data["main"]["pressure"]


def read_last():
    try:
        with open(STATE_FILE, "r") as f:
            p, t, level = f.read().split(",")
            print("📂 读取历史:", p, t, level)
            return float(p), float(t), level
    except:
        print("📂 无历史数据")
        return None


def save_current(p, t, level):
    with open(STATE_FILE, "w") as f:
        f.write(f"{p},{t},{level}")
    print("💾 已保存当前数据")


def get_level(rate):
    r = abs(rate)
    if r < 0.5:
        return "STABLE"
    elif r < 1.5:
        return "MILD"
    elif r < 3:
        return "MEDIUM"
    else:
        return "STRONG"


def check_pressure():
    print("🔥 pressure模块已执行")

    try:
        current_p = get_pressure()
        current_t = time.time()

        print(f"🌡 当前气压: {current_p} hPa")

        last = read_last()

        if not last:
            print("⚠️ 第一次运行，仅记录数据")
            save_current(current_p, current_t, "INIT")
            return

        last_p, last_t, last_level = last

        delta_p = current_p - last_p
        delta_t = (current_t - last_t) / 3600

        if delta_t <= 0:
            return

        rate = delta_p / delta_t
        level = get_level(rate)

        print(f"📈 速率: {rate:.2f} hPa/h | 等级: {level}")

        # ✅ 只在“等级变化 + 中等以上”才推送（防刷屏核心）
        if level != last_level and level in ["MEDIUM", "STRONG"]:
            direction = "📉下降" if rate < 0 else "📈上升"

            msg = (
                f"🌡气压异常 {direction}\n"
                f"速率: {rate:.2f} hPa/h\n"
                f"等级: {level}"
            )

            send_bark(msg)

        save_current(current_p, current_t, level)

    except Exception as e:
        print("❌ Pressure Error:", e)
