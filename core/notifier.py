import requests
from config import BARK_KEY
from urllib.parse import quote


def send(msg):
    print("bark send")

    try:
        # 🔥分离标题和内容（最多4行）
        lines = msg.split("\n")

        title = lines[0]
        body = "\n".join(lines[1:])

        url = (
            f"https://api.day.app/{BARK_KEY}/"
            f"{quote(title)}"
            f"?body={quote(body)}"
        )

        r = requests.get(url, timeout=10)
        print(r.status_code)

    except Exception as e:
        print("bark error", e)
