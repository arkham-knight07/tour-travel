"""
User Model - MongoDB Document
Handles user accounts, authentication, and profile management
"""
from mongoengine import Document, StringField, BooleanField, DateTimeField, EmailField, ValidationError
from datetime import datetime
from passlib.context import CryptContext

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Document):
    """User account model stored in MongoDB"""
    
    meta = {
        'collection': 'users',
        'indexes': ['email']  # Email must be unique
    }
    
    # Required fields
    name = StringField(required=True, min_length=2, max_length=100)
    email = EmailField(required=True, unique=True)  # Unique email constraint
    password_hash = StringField(required=True)
    
    # Profile information
    phone = StringField(max_length=20, default='')
    country = StringField(max_length=50, default='India')
    
    # Account status
    is_active = BooleanField(default=True)
    
    # Timestamps
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    # Save hook to update timestamp
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    def set_password(self, password: str):
        """Hash and set password using bcrypt"""
        if not password or len(password) < 6:
            raise ValidationError("Password must be at least 6 characters")
        self.password_hash = pwd_context.hash(password)
    
    def verify_password(self, password: str) -> bool:
        """Verify password against hash"""
        try:
            return pwd_context.verify(password, self.password_hash)
        except Exception:
            return False
    
    def to_dict(self):
        """Return user data as dictionary (safe for API responses - no password hash)"""
        return {
            "id": str(self.id),
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "country": self.country,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
    
    def __repr__(self):
        return f"<User {self.email}>"
    
    def __str__(self):
        return self.name
