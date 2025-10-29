from flask import Blueprint, request, jsonify
from services.tour_service import search_tours, get_tour_by_id

tours_bp = Blueprint("tours", __name__)

# List all tours or search
@tours_bp.route("/", methods=["GET"])
def list_tours():
	q = request.args.get("q", "")
	type_ = request.args.get("type", "")
	featured = request.args.get("featured")
	if featured is not None:
		featured = featured.lower() in ("1", "true", "yes")
	tours = search_tours(q=q, type_=type_, featured=featured)
	return jsonify(tours)

# Get a single tour by id
@tours_bp.route("/<tour_id>", methods=["GET"])
def get_tour(tour_id):
	tour = get_tour_by_id(tour_id)
	if tour:
		return jsonify(tour)
	return jsonify({"error": "Tour not found"}), 404
