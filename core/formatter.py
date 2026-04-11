def get_risk_color(risk):
    if risk < 30:
        return "🟢"
    elif risk < 60:
        return "🟡"
    elif risk < 80:
        return "🟠"
    else:
        return "🔴"


# =========================
# 🌬️事件符号映射（严格规则版）
# =========================
def build_event_lines(events, data):

    lines = []

    # 🌬️东北风
    if "wind_ne" in events:
        lines.append(f"💨东北风{data['wind_scale']}级")

    # 🌨️气压低
    if "pressure_low" in events:
        lines.append(f"🌨️气压低{data['pressure']}hPa")

    # 😷AQI高
    if "aqi_high" in events:
        lines.append(f"🌫️高污染AQI{data['aqi']}")

    # 🌫️湿度高
    if "humidity_high" in events:
        lines.append(f"🫧高湿度{data['humidity']}%")

    return lines


# =========================
# 🚨主输出（严格4行规则）
# =========================
def format_event(events, data, dp_level, risk):

    color = get_risk_color(risk)

    event_lines = build_event_lines(events, data)

    # =========================
    # 🟡等级规则（严格按你文档）
    # =========================
    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    elif len(events) == 2:
        level = "🟡1️⃣级气象预警🚨"
    else:
        level = "🟢单项气象预警"

    # =========================
    # 🌏组合行（必须单行）
    # =========================
    combo = "🌏环境异常组合：" + "".join(event_lines)

    # =========================
    # 📉ΔP行
    # =========================
    dp_line = f"📉{dp_level}"

    # =========================
    # 🧠风险行
    # =========================
    risk_line = f"🧠风险{color}{risk}/100"

    # =========================
    # 📦严格4行输出
    # =========================
    return "\n".join([
        level,
        dp_line,
        risk_line,
        combo
    ])


# =========================
# 🌙心跳（严格规则）
# =========================
def format_heartbeat(data, dp_level, risk):

    color = get_risk_color(risk)

    return "\n".join([
        "🌏EnvAlert☀️天气恢复正常✅",
        f"气压:{data['pressure']} 湿度:{data['humidity']}% 风:{data['wind_dir']} AQI:{data['aqi']}",
        f"📉{dp_level} 风险:{risk}{color}"
    ])
