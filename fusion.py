import time
import requests
import json
from config import *
from wind import get_wind
from pressure import get_pressure_signals
from aqi import get_aqi_signals

# ======================
# 🔔 推送
# ======================
def send(msg):
    try:
        requests.get(f"{BARK_URL}/{BARK_KEY}/{msg}", timeout=10)
    except:
        pass

# ======================
# 📁 状态（总）
# ======================
def read_state():
    try:
        return int(open(STATE_FILE).read().strip())
    except:
        return 0

def save_state(v):
    open(STATE_FILE, "w").write(str(v))

# ======================
# 🟢 恢复节流
# ======================
def read_recovery_time():
    try:
        return float(open(RECOVERY_FILE).read().strip())
    except:
        return 0

def save_recovery_time(t):
    open(RECOVERY_FILE, "w").write(str(t))

# ======================
# 🧠 信号级状态机（核心）
# ======================
def read_signal_state():
    try:
        return json.loads(open(SIGNAL_STATE_FILE).read())
    except:
        return {
            "aqi_high": False,
            "pressure_low": False,
            "wind": False
        }

def save_signal_state(s):
    open(SIGNAL_STATE_FILE, "w").write(json.dumps(s))

# ======================
# 🚀 主逻辑
# ======================
def check_all():

    wind_t = get_wind()
    low_t, pressure_drop, current_pressure = get_pressure_signals()
    aqi_high, aqi_rise, aqi = get_aqi_signals()

    last_total = read_state()
    last_signals = read_signal_state()

    # 当前状态
    current_signals = {
        "aqi_high": aqi_high,
        "pressure_low": low_t,
        "wind": wind_t
    }

    real_count = sum(current_signals.values())

    msg = None
    now = time.time()

    # ======================
    # 🔴 新风险触发（逐项判断）
    # ======================
    if not last_signals["aqi_high"] and aqi_high:
        msg = f"🚨高污染 AQI:{aqi}"

    elif not last_signals["pressure_low"] and low_t:
        msg = f"🚨气压过低 当前:{current_pressure}hPa"

    elif not last_signals["wind"] and wind_t:
        msg = "🚨东北风触发 关闭新风"

    # ======================
    # 🟢 单项恢复（只触发一次🔥）
    # ======================
    elif last_signals["aqi_high"] and not aqi_high:
        msg = f"🟢AQI恢复正常 当前:{aqi}"

    elif last_signals["pressure_low"] and not low_t:
        msg = f"🟢气压恢复 当前:{current_pressure}hPa"

    elif last_signals["wind"] and not wind_t:
        msg = "🟢风向恢复"

    # ======================
    # 🟢 全局恢复（12小时节流）
    # ======================
    elif last_total > 0 and real_count == 0:
        last_time = read_recovery_time()
        if now - last_time > 12 * 3600:
            msg = "🟢EnvAlert恢复正常"
            save_recovery_time(now)

    # ======================
    # 🟡 趋势（不影响状态🔥）
    # ======================
    elif aqi_rise:
        msg = f"⚠️AQI快速上升 当前:{aqi}"

    elif pressure_drop and wind_t:
        msg = "⚠️气压下降+东北风"

    # ======================
    # 📤 推送
    # ======================
    if msg:
        send(msg)

    # 保存状态
    save_state(real_count)
    save_signal_state(current_signals)

    # ======================
    # 🔹 调试输出
    # ======================
    print("------状态机------")
    print("上次:", last_signals)
    print("当前:", current_signals)

    print(f"🌬 风: {wind_t}")
    print(f"📊 气压: {current_pressure} (阈值:{PRESSURE_LOW}) 低压:{low_t}")
    print(f"📈 AQI: {aqi} 高污染:{aqi_high} 上升:{aqi_rise}")
    print(f"计数: {real_count}")
