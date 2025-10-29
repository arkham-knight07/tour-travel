from flask import Blueprint, request, jsonify
import os, time, uuid, json

bookings_bp = Blueprint("bookings", __name__)
BOOKINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "storage", "bookings.json")

# ensure file exists
os.makedirs(os.path.dirname(BOOKINGS_FILE), exist_ok=True)
if not os.path.exists(BOOKINGS_FILE):
    with open(BOOKINGS_FILE, "w", encoding="utf-8") as f:
        json.dump([], f)

def save_booking(data):
    with open(BOOKINGS_FILE, "r+", encoding="utf-8") as f:
        bookings = json.load(f)
        bookings.append(data)
        f.seek(0)
        json.dump(bookings, f, indent=2)

@bookings_bp.post("/")
def book_tour():
    data = request.get_json() or {}
    required = ("name", "email", "phone", "startDate", "people")
    for k in required:
        if not data.get(k):
            return jsonify({"ok": False, "error": f"Missing field: {k}"}), 400
    
    ref = f"BM{int(time.time())}-{uuid.uuid4().hex[:6].upper()}"
    data["ref"] = ref
    save_booking(data)
    
    return jsonify({"ok": True, "ref": ref, "details": data})
@bookings_bp.get("/")
def get_bookings():
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        bookings = json.load(f)
    return jsonify(bookings)