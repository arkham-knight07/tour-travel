"""
Authentication Routes - Register, Login, Profile Management
Using MongoDB (mongoengine) for flexible user storage
"""
from flask import Blueprint, request, jsonify, make_response
from datetime import datetime, timedelta
import jwt
import os
from models.user import User
from mongoengine import NotUniqueError, ValidationError as MongoValidationError

auth_bp = Blueprint("auth", __name__)

# JWT configuration
JWT_SECRET = os.getenv('JWT_SECRET', 'travelmate-secret-key-change-in-production-2024')
JWT_ALGORITHM = "HS256"
JWT_EXPIRY_HOURS = 24

def create_jwt_token(user_id: str) -> str:
    """Create JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRY_HOURS),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user():
    """Extract user from request (from cookie or Authorization header)"""
    token = None
    
    # Try to get token from HttpOnly cookie first (recommended)
    if 'auth_token' in request.cookies:
        token = request.cookies.get('auth_token')
    
    # Fallback to Authorization header
    elif request.headers.get('Authorization'):
        auth_header = request.headers.get('Authorization')
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return None
    
    if not token:
        return None
    
    payload = verify_jwt_token(token)
    if not payload:
        return None
    
    try:
        user = User.objects(id=payload['user_id']).first()
        return user
    except Exception:
        return None

# ============ ROUTES ============

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user account"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({"error": "Missing required fields: email, password, name"}), 400
        
        # Check if user already exists
        existing = User.objects(email=data['email']).first()
        if existing:
            return jsonify({"error": "Email already registered"}), 409
        
        # Create new user
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            country=data.get('country', 'India')
        )
        user.set_password(data['password'])
        
        try:
            user.save()
        except MongoValidationError as e:
            return jsonify({"error": str(e)}), 400
        except NotUniqueError:
            return jsonify({"error": "Email already exists"}), 409
        
        # Create JWT token
        token = create_jwt_token(str(user.id))
        
        # Create response with HttpOnly cookie
        response = make_response(jsonify({
            "message": "✅ User registered successfully",
            "user": user.to_dict(),
            "token": token
        }), 201)
        
        response.set_cookie(
            'auth_token',
            token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            max_age=JWT_EXPIRY_HOURS * 3600
        )
        
        return response
        
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user with email and password"""
    try:
        data = request.get_json()
        
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing email or password"}), 400
        
        # Find user by email
        user = User.objects(email=data['email']).first()
        
        if not user or not user.verify_password(data['password']):
            return jsonify({"error": "Invalid email or password"}), 401
        
        if not user.is_active:
            return jsonify({"error": "User account is inactive"}), 403
        
        # Create JWT token
        token = create_jwt_token(str(user.id))
        
        # Create response with HttpOnly cookie
        response = make_response(jsonify({
            "message": "✅ Login successful",
            "user": user.to_dict(),
            "token": token
        }), 200)
        
        response.set_cookie(
            'auth_token',
            token,
            httponly=True,
            secure=False,  # Set to True in production with HTTPS
            samesite='Lax',
            max_age=JWT_EXPIRY_HOURS * 3600
        )
        
        return response
        
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500


@auth_bp.route('/me', methods=['GET'])
def get_profile():
    """Get current user profile"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized - no valid token"}), 401
    
    return jsonify({
        "message": "✅ Profile retrieved",
        "user": user.to_dict()
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user (clear auth cookie)"""
    response = make_response(jsonify({"message": "✅ Logout successful"}), 200)
    response.delete_cookie('auth_token')
    return response


@auth_bp.route('/update', methods=['PUT'])
def update_profile():
    """Update user profile information"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized - no valid token"}), 401
    
    try:
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data and data['name']:
            user.name = data['name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'country' in data and data['country']:
            user.country = data['country']
        
        user.save()
        
        return jsonify({
            "message": "✅ Profile updated successfully",
            "user": user.to_dict()
        }), 200
        
    except MongoValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Update failed: {str(e)}"}), 500
