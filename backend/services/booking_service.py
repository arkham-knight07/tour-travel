import time, uuid

from flask import json
from utils.paths import backend_path
from utils.jsonstore import ensure_file_with_default, append_json_array
from models.booking import Booking

BOOKINGS_FILE = backend_path("storage", "bookings.json")
ensure_file_with_default(BOOKINGS_FILE, [])

REQUIRED = ("name", "email", "phone", "startDate", "people")

def create_booking(payload: dict) -> Booking:
    for k in REQUIRED:
        if not payload.get(k):
            raise ValueError(f"Missing field: {k}")

    ref = f"BM{int(time.time())}-{uuid.uuid4().hex[:6].upper()}"
    booking = Booking(
        name=payload["name"],
        email=payload["email"],
        phone=payload["phone"],
        startDate=payload["startDate"],
        people=payload["people"],
        tourId=payload.get("tourId"),
        ref=ref
    )
    append_json_array(BOOKINGS_FILE, booking.to_dict())
    return booking
def get_all_bookings() -> list[Booking]:
    with open(BOOKINGS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        return [Booking.from_dict(item) for item in data]