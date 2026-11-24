import json
import os

LIMIT = 180
WHOAMI = "dating-bio-entry"


class Courier:
    def __init__(self):
        self.home = os.path.dirname(os.path.realpath(__file__))

    def fetch(self):
        handle = open(os.path.join(self.home, "entry.txt"), encoding="utf-8")
        payload = handle.read().strip()
        handle.close()
        if not payload or len(payload) > LIMIT:
            raise RuntimeError("payload outside gate")
        return payload

    def ship(self, payload):
        base = os.environ.get("MAKEFUN_OUTPUT_DIR") or "output"
        if not os.path.isdir(base):
            os.makedirs(base)
        spot = os.path.join(base, "entry.txt")
        blob = open(spot, "w", encoding="utf-8", newline="\n")
        blob.write(payload + "\n")
        blob.close()
        back = open(spot, encoding="utf-8")
        same = back.read().strip() == payload
        back.close()
        if not same:
            raise RuntimeError("mismatch after write")
        return spot


if __name__ == "__main__":
    courier = Courier()
    payload = courier.fetch()
    spot = courier.ship(payload)
    print(json.dumps({"gate": "pass", "size": len(payload), "echo": spot, "who": WHOAMI}))
