import os, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json(relpath):
    file_path = os.path.join(BASE, relpath)
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    return {} 