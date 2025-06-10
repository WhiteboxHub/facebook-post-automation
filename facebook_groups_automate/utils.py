import random
import time
import os
import json
from datetime import datetime

def human_delay(a=2, b=5):
    """Random delay to mimic human behavior."""
    time.sleep(random.uniform(a, b))

def log(message):
    print(f"[INFO] {message}")

def get_last_run(path="last_run.json"):
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("last_run")

def set_last_run(path="last_run.json"):
    now = datetime.now().isoformat(timespec='seconds')
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"last_run": now}, f)
    return now 