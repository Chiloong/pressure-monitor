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
    if os.path.exists(STATE_FILE):
        return int(open(STATE_FILE).read().strip())
    return 0

def save_state(v):
    open(STATE_FILE, "w").write(str(v))

def check_all():

    wind_t = get_wind()
    low_t, rate_t = get_pressure_signals()
    aqi_t = get_aqi()

    count = sum([wind_t, low_t, rate_t, aqi_t])
    last = read_state()

    msg = None

    if count > last:

        if count == 1:
            if wind_t:
                msg = "🚨EnvAlert🚨\n🏭发电厂↙️东北风💨触发\n⛔️关闭新风🟣颗粒过滤开大⬆️"
            elif low_t:
                msg = "🚨EnvAlert🚨\n✴️气压🌨️过低🥱"
            elif rate_t:
                msg = "🚨EnvAlert🚨\n✴️气压〽️骤变😣"
            elif aqi_t:
                msg = "🚨EnvAlert🚨\n🟥高污染😷"

        elif count == 2:
            msg = "🟡气象预警🚨"
        elif count == 3:
            msg = "🟠气象预警🚨"
        elif count == 4:
            msg = "🔴气象预警🚨"

    if msg:
        send(msg)

    save_state(count)

    print(f"当前:{count} 上次:{last}")
