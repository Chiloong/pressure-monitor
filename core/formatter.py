def format_event(events, data, dp_level, risk):

    # 🔴多事件等级
    level = ""

    if len(events) >= 4:
        level = "🔴3️⃣级气象预警🚨"
    elif len(events) == 3:
        level = "🟠2️⃣级气象预警🚨"
    elif len(events) == 2:
        level = "🟡1️⃣级气象预警🚨"

    # 🚨基础标题
    lines = ["🚨EnvAlert🚨"]

    # 🔥事件映射（按优先级）
    if "wind_ne" in events:
        lines.append(f"🏭发电厂↙️东北风{data['wind_scale']}级💨")

    if "pressure_low" in events:
        lines.append(f"✴️气压🌨️过低🥱{data['pressure']}hPa")

    if "aqi_high" in events:
        lines.append(f"🟥高污染🌫️AQI{data['aqi']}😷")

    if "humidity_high" in events:
        lines.append(f"✴️湿度🫧过高😶‍🌫️{data['humidity']}%")

    # 📉ΔP + 风险
    lines.append(f"📉ΔP:{dp_level} 🧠风险{risk}")

    # 🔴多事件覆盖（最高优先级）
    if level:
        return "\n".join([
            level,
            f"📉{dp_level}",
            f"🧠风险{risk}",
            f"🌏环境异常组合"
        ])

    # 📏强制4行限制
    return "\n".join(lines[:4])


def format_heartbeat(data, dp_level, risk):

    return (
        "🌏EnvAlert☀️天气恢复正常✅\n"
        f"气压{data['pressure']} 湿度{data['humidity']}% 风{data['wind_dir']} AQI{data['aqi']}\n"
        f"📉{dp_level} 🧠风险{risk}"
    )
