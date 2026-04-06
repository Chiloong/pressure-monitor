def check_fusion():
    print("🧠 联动模块运行")
    from wind import check_wind
    from pressure import check_pressure

    speed, deg = check_wind()
    pressure = check_pressure()

    # 简单趋势逻辑示例
    trend = "STABLE"
    if pressure is not None:
        if pressure < 1005:
            trend = "LOW_PRESSURE"
        elif pressure > 1020:
            trend = "HIGH_PRESSURE"

    print(f"🌬 风速:{speed} | 风向:{deg}")
    print(f"🌡 气压:{pressure} | 等级: {trend}")

    # 异常联动提醒
    if trend != "STABLE" and speed > 2.5:
        msg = f"⚠️ 联动预警：气压{trend} + 风速{speed:.2f}ms"
        from pressure import send_bark
        send_bark(msg)
