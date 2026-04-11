def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"

def map_event(e, data):
    mapping = {
        "wind_ne":        "💨东北风",
        "pressure_low":   "🌨️气压低",
        "aqi_high":       "🌫️高污染",
        "humidity_high":  "🫧高湿度",
        "pressure_change":"〽️气压降",
    }
    return mapping.get(e, "")

def format_event(events, data, dp_level, risk):
    color = get_risk_color(risk)

    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    elif len(events) == 2:
        level = "🟡1️⃣级气象预警🚨"
    else:
        level = "🟢单项气象预警"

    event_text = "".join(map_event(e, data) for e in events)

    return "\n".join([
        level,
        f"📉{dp_level}",
        f"🧠风险{color}{risk}/100",
        f"🌏异常：{event_text}"
    ])

def format_heartbeat(data, dp_level, risk):
    color = get_risk_color(risk)
    return "\n".join([
        "🌏EnvAlert 定时播报",   # 修复：心跳不代表恢复正常
        f"气压:{data['pressure']} 湿度:{data['humidity']}% 风:{data['wind_dir']} AQI:{data['aqi']}",
        f"📉{dp_level} 风险:{risk}{color}"
    ])
