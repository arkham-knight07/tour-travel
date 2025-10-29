from flask import Blueprint, jsonify, request
from services.booking_service import create_booking, get_all_bookings

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/", methods=["POST"])
def book_tour():
    data = request.get_json() or {}
    try:
        booking = create_booking(data)
        return jsonify({"ok": True, "ref": booking.ref, "details": booking.to_dict()})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400

@booking_bp.route("/", methods=["GET"])
def list_bookings():
    bookings = get_all_bookings()
    return jsonify([b.to_dict() for b in bookings])
