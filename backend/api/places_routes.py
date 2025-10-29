"""
Places Routes - CRUD operations for destinations, treks, and places
Using MongoDB (mongoengine) for flexible place data storage
"""
from flask import Blueprint, request, jsonify
from models.place import Place
from mongoengine import ValidationError, NotUniqueError, Q

places_bp = Blueprint("places", __name__)

# ============ ROUTES ============

@places_bp.route('/', methods=['GET'])
def get_places():
    """
    Get all places with optional filtering and pagination
    Query params: category, featured, page, limit
    """
    try:
        # Query parameters
        category = request.args.get('category', None)  # 'destination', 'trek', 'international'
        featured_only = request.args.get('featured', 'false').lower() == 'true'
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        # Build query
        query = Place.objects()
        
        if category and category in ['destination', 'trek', 'international']:
            query = query.filter(category=category)
        
        if featured_only:
            query = query.filter(is_featured=1)
        
        # Pagination
        total = query.count()
        skip = (page - 1) * limit
        places = query.skip(skip).limit(limit).order_by('-created_at')
        
        return jsonify({
            "status": "success",
            "places": [place.to_dict() for place in places],
            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "pages": (total + limit - 1) // limit
            }
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@places_bp.route('/<place_id>', methods=['GET'])
def get_place(place_id):
    """Get a specific place by ID"""
    try:
        place = Place.objects(id=place_id).first()
        
        if not place:
            return jsonify({"status": "error", "error": "Place not found"}), 404
        
        return jsonify({
            "status": "success",
            "place": place.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@places_bp.route('/search', methods=['GET'])
def search_places():
    """
    Search places by name or location
    Query param: q (search term, minimum 2 characters)
    """
    try:
        search_term = request.args.get('q', '').strip()
        
        if not search_term or len(search_term) < 2:
            return jsonify({"status": "error", "error": "Search term too short (min 2 chars)"}), 400
        
        # Search in name and location_name using regex
        places = Place.objects(
            Q(name__icontains=search_term) | 
            Q(location_name__icontains=search_term) |
            Q(description__icontains=search_term)
        ).limit(10)
        
        return jsonify({
            "status": "success",
            "query": search_term,
            "results": [place.to_dict() for place in places],
            "count": len(list(places))
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@places_bp.route('/', methods=['POST'])
def create_place():
    """
    Create a new place/destination
    Required: name, location_name, latitude, longitude
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['name', 'location_name', 'latitude', 'longitude']
        missing = [f for f in required if f not in data]
        if missing:
            return jsonify({"status": "error", "error": f"Missing fields: {', '.join(missing)}"}), 400
        
        # Create new place
        place = Place(
            name=data['name'],
            location_name=data['location_name'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            description=data.get('description', ''),
            category=data.get('category', 'destination'),
            image_url=data.get('image_url', ''),
            price=data.get('price', '₹0'),
            is_featured=1 if data.get('is_featured', False) else 0,
            rating=float(data.get('rating', 0.0)),
            review_count=int(data.get('review_count', 0))
        )
        
        # Validate and save
        place.clean()
        place.save()
        
        return jsonify({
            "status": "success",
            "message": "✅ Place created successfully",
            "place": place.to_dict()
        }), 201
        
    except NotUniqueError:
        return jsonify({"status": "error", "error": "Place name already exists"}), 409
    except ValidationError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@places_bp.route('/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a place"""
    try:
        place = Place.objects(id=place_id).first()
        
        if not place:
            return jsonify({"status": "error", "error": "Place not found"}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'name' in data and data['name']:
            place.name = data['name']
        if 'description' in data:
            place.description = data['description']
        if 'price' in data:
            place.price = data['price']
        if 'image_url' in data:
            place.image_url = data['image_url']
        if 'rating' in data:
            place.rating = float(data['rating'])
        if 'review_count' in data:
            place.review_count = int(data['review_count'])
        if 'is_featured' in data:
            place.is_featured = 1 if data['is_featured'] else 0
        
        place.save()
        
        return jsonify({
            "status": "success",
            "message": "✅ Place updated successfully",
            "place": place.to_dict()
        }), 200
        
    except ValidationError as e:
        return jsonify({"status": "error", "error": str(e)}), 400
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@places_bp.route('/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a place"""
    try:
        place = Place.objects(id=place_id).first()
        
        if not place:
            return jsonify({"status": "error", "error": "Place not found"}), 404
        
        place.delete()
        
        return jsonify({
            "status": "success",
            "message": "✅ Place deleted successfully"
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
