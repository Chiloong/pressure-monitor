# main.py
from wind import get_wind
from pressure import check_pressure_and_wind

def main():
    print("🧠 联动模块运行")
    try:
        # 获取风速和风向
        wind_speed, wind_dir = get_wind()
        print(f"🌬 风速:{wind_speed:.2f} | 风向:{wind_dir:.0f}")

        # 检查气压趋势并根据风信息进行联动
        check_pressure_and_wind(wind_speed, wind_dir)

    except Exception as e:
        print("❌ Main Error:", e)


if __name__ == "__main__":
    main()
