from flask import Blueprint, request, jsonify
from services.chatbot_service import reply_to

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/", methods=["POST"])
def chat():
    data = request.get_json() or {}
    msg = data.get("message", "")
    reply = reply_to(msg)
    return jsonify({"reply": reply})