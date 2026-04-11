def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"


def format_event(events, data, dp_level, risk):

    color = get_risk_color(risk)

    # ===== 事件映射 =====
    event_map = {
        "wind_ne": ("💨东北风", 1),
        "aqi_high": ("🌫️高污染", 2),
        "pressure_change": ("〽️气压变", 3),
        "pressure_low": ("🌨️气压低", 4),
        "humidity_high": ("🫧高湿度", 5),
    }

    # ===== 排序 =====
    event_list = []
    for e in events:
        if e in event_map:
            event_list.append(event_map[e])

    event_list = sorted(event_list, key=lambda x: x[1])

    # ===== 核心修复：组合文本 =====
    event_text = "".join([e[0] for e in event_list])

    # ===== 级别判断 =====
    level = ""
    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    elif len(events) == 2:
        level = "🟡1️⃣级气象预警🚨"

    # ===== 单事件详细 =====
    lines = ["🚨EnvAlert🚨"]

    if "wind_ne" in events:
        lines.append(f"🏭东北风{data['wind_scale']}级💨")

    if "pressure_low" in events:
        lines.append(f"🌨️气压过低🥱{data['pressure']}hPa")

    if "aqi_high" in events:
        lines.append(f"🌫️高污染AQI{data['aqi']}😷")

    if "humidity_high" in events:
        lines.append(f"🫧湿度过高{data['humidity']}%")

    lines.append(f"📉{dp_level} 🧠风险{color}{risk}/100")

    # ===== 组合输出（关键修复点）=====
    if level:
        return "\n".join([
            level,
            f"📉{dp_level}",
            f"🧠风险{color}{risk}/100",
            f"🌏环境异常组合：{event_text}"
        ])

    return "\n".join(lines[:4])
