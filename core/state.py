import json, os, time

STATE_FILE = "storage/event_state.json"
HEARTBEAT_FILE = "storage/heartbeat.json"


def load(path, default):
    if not os.path.exists(path):
        return default
    try:
        return json.load(open(path))
    except:
        return default


def save(path, data):
    json.dump(data, open(path, "w"))


# =========================
# 🔥统一冷却系统（关键修复）
# =========================
def can_trigger(key, cooldown=1800):

    state = load(STATE_FILE, {})
    now = time.time()

    last = state.get(key, 0)

    if now - last < cooldown:
        return False

    state[key] = now
    save(STATE_FILE, state)

    return True


def heartbeat_due(interval):
    hb = load(HEARTBEAT_FILE, {"t": 0})
    now = time.time()

    if now - hb["t"] > interval:
        hb["t"] = now
        save(HEARTBEAT_FILE, hb)
        return True

    return False
