# ✅aqi.py 完整替换版（趋势预警支持）

```python
import requests
import time
import os
from config import *

def load_last():
    try:
        with open(AQI_STATE_FILE, "r") as f:
            aqi, t = f.read().split(",")
            return float(aqi), float(t)
    except:
        return None

def save(aqi, t):
    with open(AQI_STATE_FILE, "w") as f:
        f.write(f"{aqi},{t}")

def get_aqi_signals():
    try:
        url = WAQI_URL.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
        data = requests.get(url, timeout=10).json()

        if data.get("status") != "ok":
            print("❌ AQI接口异常")
            return False, False, 0

        aqi = data["data"]["aqi"]
        now = time.time()

        last = load_last()

        rise_trigger = False

        if last:
            last_aqi, last_t = last
            dt = (now - last_t) / 3600

            if dt > 0:
                delta = aqi - last_aqi
                rate = delta / dt

                print(f"📈 AQI变化速率:{rate:.2f}/h")

                if rate > AQI_DELTA_THRESHOLD:
                    rise_trigger = True

        save(aqi, now)

        high_trigger = aqi >= AQI_THRESHOLD

        print(f"🟥 AQI:{aqi} 高污染:{high_trigger} 上升预警:{rise_trigger}")

        return high_trigger, rise_trigger, aqi

    except Exception as e:
        print("❌ AQI Error:", e)
        return False, False, 0
```
