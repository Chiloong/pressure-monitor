print("=== RUNNING ===")

from core.sensor import fetch_all
from core.engine import detect
from core.state import can_trigger_event, heartbeat_due
from core.formatter import format_event, format_heartbeat
from core.notifier import send
from config import HEARTBEAT_INTERVAL
import json, os


def log(msg):
    print(f"[EnvAlert] {msg}")


def main():

    log("🚀 start")

    data = fetch_all()
    log(f"data={data}")

    if not data:
        log("ERROR empty data")
        return

    os.makedirs("storage", exist_ok=True)

    prev = None
    if os.path.exists("storage/state.json"):
        try:
            prev = json.load(open("storage/state.json"))
        except:
            prev = None

    events, dp_level, risk = detect(data, prev)

    print("events =", events)

    json.dump(data, open("storage/state.json", "w"))

    # =========================
    # 🌙心跳
    # =========================
    if heartbeat_due(HEARTBEAT_INTERVAL):
        msg = format_heartbeat(data, dp_level, risk)
        log("heartbeat")
        send(msg)

    # =========================
    # 🔥核心修复：统一事件推送（关键）
    # =========================
    if events:

        if can_trigger_event("combo:" + ",".join(sorted(events))):

            msg = format_event(events, data, dp_level, risk)

            log(f"event_push={events}")

            send(msg)


if __name__ == "__main__":
    main()
