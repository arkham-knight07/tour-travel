from flask import Flask, jsonify
from flask_cors import CORS
from config.database import init_db, check_connection
from api.booking_routes import booking_bp
from api.chatbot_routes import chatbot_bp
from api.tours_routes import tours_bp
from api.auth_routes import auth_bp
from api.places_routes import places_bp

def create_app():
    app = Flask(__name__)
    
    # Enable CORS
    from flask_cors import CORS
    CORS(app)

    @app.route("/")
    def index():
        return jsonify({"ok": True, "service": "TravelMate API 🚀", "status": "running"})
    
    @app.route("/health")
    def health():
        """Health check endpoint"""
        db_ok = check_connection()
        return jsonify({
            "service": "TravelMate API",
            "status": "healthy" if db_ok else "degraded",
            "database": "connected" if db_ok else "disconnected",
            "api": "operational"
        })

    # Existing blueprints (unchanged - use JSON files)
    app.register_blueprint(booking_bp, url_prefix="/api/bookings")
    app.register_blueprint(chatbot_bp, url_prefix="/chat")
    app.register_blueprint(tours_bp, url_prefix="/api/tours")
    print("✅ Existing routes loaded (bookings, chatbot, tours)")
    
    # New blueprints for auth and places (MongoDB-backed)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(places_bp, url_prefix="/api/places")
    print("✅ Auth routes loaded")
    print("✅ Places routes loaded")

    return app

if __name__ == "__main__":
    app = create_app()
    port = 5002  # Try port 5002 if 5001 is busy
    print("\n🚀 Starting TravelMate API Server...")
    print(f"📍 Available at: http://127.0.0.1:{port}")
    print(f"📚 API Docs at: http://127.0.0.1:{port}/health\n")
    app.run(debug=True, port=port)
