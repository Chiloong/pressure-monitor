import os

# 🌍 数据源配置
OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
BARK_URL = "https://api.day.app"

# 📍 地点
LAT = 35.21
LON = 113.29

# 🔑 Secrets (环境变量)
API_KEY = os.environ.get("API_KEY")
BARK_KEY = os.environ.get("BARK_KEY")

# ⚖️ 阈值
PRESSURE_RATE_THRESHOLD = 1.0      # hPa/h，气压变化率报警阈值
WIND_SPEED_THRESHOLD = 5.0         # m/s，风速报警阈值
WIND_GUST_THRESHOLD = 8.0          # m/s，阵风阈值
WIND_NE_MIN = 20                    # °东北风最小角度
WIND_NE_MAX = 100                   # °东北风最大角度
