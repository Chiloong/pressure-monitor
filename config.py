import os

# ======================
# 🌍 QWeather
# ======================
QWEATHER_API_KEY = os.environ.get("QWEATHER_API_KEY")
QWEATHER_NOW = "https://devapi.qweather.com/v7/weather/now"
QWEATHER_AIR = "https://devapi.qweather.com/v7/air/now"

BARK_URL = "https://api.day.app"
BARK_KEY = os.environ.get("BARK_KEY")

# ======================
# 📍 地点
# ======================
LAT = 35.21
LON = 113.29

# ======================
# ⚖️ 阈值
# ======================
WIND_SPEED_THRESHOLD = 2.5
NE_MIN = 20
NE_MAX = 100

PRESSURE_LOW = 1000
PRESSURE_RATE_THRESHOLD = 1.0

AQI_THRESHOLD = 180
AQI_DELTA_THRESHOLD = 15

HUMIDITY_THRESHOLD = 60

# ======================
# 📁 状态
# ======================
STATE_FILE = "fusion_state.txt"
SIGNAL_STATE_FILE = "signal_state.txt"
RECOVERY_FILE = "recovery_state.txt"

PRESSURE_FILE = "pressure_state.txt"
AQI_STATE_FILE = "aqi_state.txt"

RUN_STATE_FILE = "run_state.txt"
