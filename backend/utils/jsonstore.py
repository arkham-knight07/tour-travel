import json, os
from .paths import backend_path, frontend_path

def load_json_any(*candidate_relpaths):
    """
    Tries backend first (backend/<relpath>), then frontend (frontend/<relpath>).
    Returns Python object; raises FileNotFoundError if none exist.
    """
    tried = []
    for rel in candidate_relpaths:
        p1 = backend_path(rel)
        p2 = frontend_path(rel)
        for p in (p1, p2):
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    return json.load(f)
            tried.append(p)
    raise FileNotFoundError("None of these files exist: " + " | ".join(tried))

def ensure_file_with_default(abs_path, default_obj):
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    if not os.path.exists(abs_path):
        with open(abs_path, "w", encoding="utf-8") as f:
            json.dump(default_obj, f, indent=2)

def append_json_array(abs_path, obj):
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    if not os.path.exists(abs_path):
        with open(abs_path, "w", encoding="utf-8") as f:
            json.dump([obj], f, indent=2)
        return
    with open(abs_path, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if not isinstance(data, list):
                data = []
        except json.JSONDecodeError:
            data = []
        data.append(obj)
        f.seek(0)
        f.truncate()
        json.dump(data, f, indent=2)
def load_json(relpath):
    file_path = backend_path(relpath)
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)