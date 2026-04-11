from core.sensor import fetch_all
from core.engine import detect
from core.state import can_trigger, heartbeat_due
from core.formatter import format_event, format_heartbeat
from core.notifier import send
from config import HEARTBEAT_INTERVAL


def main():
    data = fetch_all()

    try:
        import json, os
        prev = json.load(open("storage/state.json"))
    except:
        prev = None

    events, dp_level = detect(data, prev)

    # 💾更新状态
    import json
    os.makedirs("storage", exist_ok=True)
    json.dump(data, open("storage/state.json", "w"))

    risk = 50  # 预留（后续升级）

    # 🌙心跳模式
    if heartbeat_due(HEARTBEAT_INTERVAL):
        msg = format_heartbeat(data, dp_level, risk)
        send(msg)
        return

    # 🚨事件模式
    if len(events) > 0:
        if can_trigger(str(events)):
            msg = format_event(events, data, dp_level)
            send(msg)


if __name__ == "__main__":
    main()
