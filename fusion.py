import requests
import os
import json

LAT = 35.21
LON = 113.29

QWEATHER_API = "https://devapi.qweather.com/v7/weather/now"
WAQI_API = "https://api.waqi.info/feed/geo:{lat};{lon}/?token={token}"

QWEATHER_KEY = os.environ.get("QWEATHER_KEY")
WAQI_TOKEN = os.environ.get("WAQI_TOKEN")


def fetch_all():
    print("🌍 开始获取数据...")

    weather_url = f"{QWEATHER_API}?location={LON},{LAT}&key={QWEATHER_KEY}"
    print("🔑 KEY:", "***" if QWEATHER_KEY else None)
    print("🌐 URL:", weather_url)

    try:
        weather = requests.get(weather_url, timeout=10).json()
    except Exception as e:
        print("❌ QWeather请求失败:", e)
        return None

    print("📦 QWeather返回:", weather)

    if not weather or weather.get("code") != "200" or "now" not in weather:
        print("❌ QWeather数据异常")
        return None

    now = weather["now"]

    pressure = float(now.get("pressure", 0))
    humidity = float(now.get("humidity", 0))
    wind_speed = float(now.get("windSpeed", 0))
    wind_dir = now.get("windDir", "")
    wind_scale = now.get("windScale", "")

    aqi = 0
    try:
        waqi_url = WAQI_API.format(lat=LAT, lon=LON, token=WAQI_TOKEN)
        waqi = requests.get(waqi_url, timeout=10).json()

        print("📦 WAQI返回:", waqi)

        if waqi.get("status") == "ok":
            aqi = waqi["data"]["aqi"]
    except Exception as e:
        print("⚠️ WAQI请求失败:", e)

    return {
        "pressure": pressure,
        "humidity": humidity,
        "wind_speed": wind_speed,
        "wind_dir": wind_dir,
        "wind_scale": wind_scale,
        "aqi": aqi
    }


STATE_FILE = "state.json"


def load_state():
    if not os.path.exists(STATE_FILE):
        return []
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_state(data):
    history = load_state()
    history.append(data)
    history = history[-72:]

    with open(STATE_FILE, "w") as f:
        json.dump(history, f)


def calc_trend(history):
    if len(history) < 5:
        return "📈12h趋势: 数据积累中"

    pressures = [x.get("pressure", 0) for x in history]
    aqis = [x.get("aqi", 0) for x in history]

    dp = pressures[-1] - pressures[0]
    daqi = aqis[-1] - aqis[0]

    return (
        "📈12h趋势\n"
        f"气压变化:{dp:+.1f} hPa\n"
        f"AQI变化:{daqi:+.0f}"
    )


def send_bark(msg):
    BARK_KEY = os.environ.get("BARK_KEY")
    if not BARK_KEY:
        print("❌ 没有BARK_KEY")
        return

    # ❗关键修复：不做任何编码处理
    url = f"https://api.day.app/{BARK_KEY}/{msg}"

    try:
        requests.get(url, timeout=10)
        print("📲 已推送")
    except Exception as e:
        print("❌ 推送失败:", e)


def check_all():
    data = fetch_all()

    if not data:
        print("❌ 数据获取失败，终止")
        return

    save_state(data)
    history = load_state()

    trend = calc_trend(history)

    msg = "\n".join([
        "🌍环境监测",
        f"气压:{data['pressure']}",
        f"湿度:{data['humidity']}%",
        f"风:{data['wind_dir']} {data['wind_scale']}级 ({data['wind_speed']})",
        f"AQI:{data['aqi']}",
        "",
        trend
    ])

    print("📨 推送内容:\n", msg)

    send_bark(msg)
