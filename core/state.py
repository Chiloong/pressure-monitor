import json, os, time

STATE_FILE = "storage/event_state.json"
HEARTBEAT_FILE = "storage/heartbeat.json"


def load(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return default


def safe_save(path, data):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(data, f)
    except Exception as e:
        print("[State] save error:", e)


def can_trigger(key, cooldown=1800):

    state = load(STATE_FILE, {})
    now = time.time()

    last = state.get(key, 0)

    if now - last < cooldown:
        return False

    state[key] = now
    safe_save(STATE_FILE, state)

    return True


def heartbeat_due(interval):
    hb = load(HEARTBEAT_FILE, {"t": 0})
    now = time.time()

    if now - hb["t"] > interval:
        hb["t"] = now
        safe_save(HEARTBEAT_FILE, hb)
        return True

    return False
