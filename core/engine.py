def detect(data, prev):
    events = []

    angle = data.get("wind_angle", 0)

    if 20 <= angle <= 100:
        events.append("wind_ne")

    if data["pressure"] < PRESSURE_LOW:
        events.append("pressure_low")

    if data["aqi"] > AQI_HIGH:
        events.append("aqi_high")

    if data["humidity"] > HUMIDITY_HIGH:
        events.append("humidity_high")

    # ΔP
    if prev:
        dp = data["pressure"] - prev["pressure"]
        dp_abs = abs(dp)

        if dp_abs < DP_WEAK:
            dp_level = "🟢弱波动"
        elif dp_abs < DP_STRONG:
            dp_level = "🟡中波动"
        else:
            dp_level = "🔴强波动"
    else:
        dp_level = "🟢弱波动"

    # 🧠风险
    risk = 0

    weight = {
        "pressure_low": 30,
        "aqi_high": 30,
        "humidity_high": 20,
        "wind_ne": 20
    }

    for e in events:
        risk += weight.get(e, 10)

    if "🔴" in dp_level:
        risk += 20
    elif "🟡" in dp_level:
        risk += 10

    risk = min(risk, 100)

    # 🔥关键：排序（稳定输出）
    priority = {
        "wind_ne": 1,
        "aqi_high": 2,
        "pressure_change": 3,
        "pressure_low": 4,
        "humidity_high": 5
    }

    events.sort(key=lambda x: priority.get(x, 99))

    return events, dp_level, risk
