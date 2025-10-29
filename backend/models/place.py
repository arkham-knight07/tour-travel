"""
Place Model - MongoDB Document
Handles destinations, treks, and international places for the globe
"""
from mongoengine import Document, StringField, FloatField, IntField, DateTimeField, ValidationError
from datetime import datetime

class Place(Document):
    """Place/Destination model stored in MongoDB"""
    
    meta = {
        'collection': 'places',
        'indexes': ['name', 'category', 'is_featured']  # Common query fields
    }
    
    # Required fields
    name = StringField(required=True, unique=True, max_length=200)  # e.g., "Goa, India"
    location_name = StringField(required=True, max_length=100)  # e.g., "Goa"
    
    # Geographic coordinates (for globe)
    latitude = FloatField(required=True)  # -90 to 90
    longitude = FloatField(required=True)  # -180 to 180
    
    # Place details
    description = StringField(default='')  # Long text description
    category = StringField(choices=['destination', 'trek', 'international'], default='destination')
    image_url = StringField(default='')  # URL to place image
    price = StringField(default='₹0')  # e.g., "₹8,999"
    
    # Metadata
    is_featured = IntField(choices=[0, 1], default=0)  # 1 = featured, 0 = not featured
    rating = FloatField(default=0.0, min_value=0, max_value=5)  # 0-5 star rating
    review_count = IntField(default=0, min_value=0)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    # Save hook to update timestamp
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def clean(self):
        """Validate coordinates"""
        if self.latitude < -90 or self.latitude > 90:
            raise ValidationError("Latitude must be between -90 and 90")
        if self.longitude < -180 or self.longitude > 180:
            raise ValidationError("Longitude must be between -180 and 180")
    
    def to_dict(self):
        """Return place data as dictionary for API responses"""
        return {
            "id": str(self.id),
            "name": self.name,
            "location_name": self.location_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "description": self.description,
            "category": self.category,
            "image_url": self.image_url,
            "price": self.price,
            "is_featured": bool(self.is_featured),
            "rating": self.rating,
            "review_count": self.review_count,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<Place {self.name}>"
    
    def __str__(self):
        return self.name
