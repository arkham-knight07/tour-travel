from flask import Blueprint, request, jsonify
from utils.helpers import load_json

tours_bp = Blueprint("tours", __name__)

TOURS = load_json("data/tours.json")

def search_tours(q="", type_=""):
    q = (q or "").lower().strip()
    type_ = (type_ or "").lower().strip()
    results = []
    for t in TOURS:
        ok = True
        if q:
            ok &= q in t["title"].lower() or q in t.get("short", "").lower()
        if type_:
            ok &= t["type"].lower() == type_
        if ok:
            results.append(t)
    return results

@tours_bp.get("/")
def get_tours():
    featured = request.args.get("featured")
    q = request.args.get("q", "")
    type_ = request.args.get("type", "")
    items = search_tours(q, type_)
    if featured:
        items = [i for i in items if i.get("featured")]
    return jsonify(items)
@tours_bp.get("/<int:tour_id>")
def get_tour(tour_id):
    tour = next((t for t in TOURS if t["id"] == tour_id), None)
    if tour:
        return jsonify(tour)
    return jsonify({"error": "Tour not found"}), 404