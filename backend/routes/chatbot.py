from flask import Blueprint, request, jsonify
from utils.helpers import load_json

chatbot_bp = Blueprint("chatbot", __name__)
FAQ = load_json("data/faq.json")

@chatbot_bp.post("/")
def chat():
    data = request.get_json() or {}
    msg = (data.get("message") or "").lower()
    
    # exact match
    for key, ans in FAQ.items():
        if key in msg:
            return jsonify({"reply": ans})

    # fuzzy match
    words = set(w.strip(".,!?") for w in msg.split() if w)
    best_key, best_score = None, 0
    for key in FAQ:
        score = len(words.intersection(set(key.split())))
        if score > best_score:
            best_key, best_score = key, score
    if best_key:
        return jsonify({"reply": FAQ[best_key]})

    return jsonify({"reply": "I can help with booking, payment, refund, cancellation or visa. What would you like to know?"})
@chatbot_bp.get("/faq")
def get_faq():
    return jsonify(FAQ)

from .. import create_app  # Use relative import since this file is inside backend/routes

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)