import os
import requests
from config import *
from wind import get_wind
from pressure import get_pressure_signals
from aqi import get_aqi

def send(msg):
    try:
        requests.get(f"{BARK_URL}/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

def read_state():
    if not os.path.exists(STATE_FILE):
        return 0

    try:
        content = open(STATE_FILE).read().strip()

        if content == "ON":
            return 1
        if content == "OFF":
            return 0

        return int(content)
    except:
        return 0

def save_state(v):
    try:
        with open(STATE_FILE, "w") as f:
            f.write(str(v))
    except:
        pass

def check_all():

    wind_t = get_wind()
    low_t, rate_t = get_pressure_signals()
    aqi_t, aqi = get_aqi()

    count = sum([wind_t, low_t, rate_t, aqi_t])
    last = read_state()

    msg = None

    # ======================
    # 🚨 升级触发
    # ======================
    if count > last:

        if count == 1:
            if wind_t:
                msg = "🚨EnvAlert🚨\n🏭发电厂↙️东北风💨触发\n⛔️关闭新风🟣颗粒过滤开大⬆️"
            elif low_t:
                msg = "🚨EnvAlert🚨\n✴️气压🌨️过低🥱"
            elif rate_t:
                msg = "🚨EnvAlert🚨\n✴️气压〽️骤变😣"
            elif aqi_t:
                msg = f"🚨EnvAlert🚨\n🟥高污染AQI{aqi}+😷"

        elif count == 2:
            msg = "🟡气象预警🚨"
        elif count == 3:
            msg = "🟠气象预警🚨"
        elif count == 4:
            msg = "🔴气象预警🚨"

    # ======================
    # 🟢 恢复提醒（新增）
    # ======================
    elif count < last:

        if count == 0:
            msg = "🟢EnvAlert恢复正常"

        elif last >= 2 and count == 1:
            msg = "🟢气象风险下降"

    # ======================
    # 🔔 发送
    # ======================
    if msg:
        send(msg)

    save_state(count)

    print(f"当前:{count} 上次:{last}")
