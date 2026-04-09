import os

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BARK_URL = "https://api.day.app"

# 🌫 WAQI（真实AQI）
WAQI_URL = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"
WAQI_TOKEN = os.environ.get("WAQI_TOKEN")

LAT = 35.21
LON = 113.29

API_KEY = os.environ.get("API_KEY")
BARK_KEY = os.environ.get("BARK_KEY")

# 阈值
PRESSURE_LOW = 990
PRESSURE_RATE_THRESHOLD = 1.0

WIND_SPEED_THRESHOLD = 2.5
GUST_THRESHOLD = 4.0
NE_MIN = 20
NE_MAX = 100

AQI_THRESHOLD = 180  # ✅ 真实AQI阈值

STATE_FILE = "fusion_state.txt"
PRESSURE_FILE = "pressure_state.txt"
