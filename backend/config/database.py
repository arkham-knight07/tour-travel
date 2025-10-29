"""
MongoDB Database Configuration
Using mongoengine for flexible, programmer-friendly ORM
Supports both local MongoDB and MongoDB Atlas cloud
"""
import os
from dotenv import load_dotenv
from mongoengine import connect, disconnect
import pymongo

load_dotenv()

# MongoDB Connection Configuration
# Default: Local MongoDB on localhost:27017
# For production: Use MongoDB Atlas connection string
MONGO_URI = os.getenv(
    'MONGODB_URI',
    'mongodb://localhost:27017/travelmate'
)

# Optional: MongoDB Atlas (cloud)
# MONGO_URI = os.getenv(
#     'MONGODB_URI',
#     'mongodb+srv://username:password@cluster.mongodb.net/travelmate?retryWrites=true&w=majority'
# )

def init_db(app):
    """Initialize MongoDB connection with Flask app"""
    try:
        # Disconnect any existing connection
        disconnect()
        
        # Connect to MongoDB
        connect(
            host=MONGO_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            retryWrites=True
        )
        
        print(f"✅ MongoDB connected: {MONGO_URI}")
        print("✅ Database ready for collections (auto-created on first use)")
        
        return True
    except Exception as e:
        print(f"❌ MongoDB connection error: {str(e)}")
        print("💡 Make sure MongoDB is running locally or update MONGODB_URI in .env")
        return False

def check_connection():
    """Check if MongoDB is accessible"""
    try:
        client = pymongo.MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()  # Will raise exception if can't connect
        return True
    except Exception as e:
        print(f"❌ Cannot connect to MongoDB: {str(e)}")
        return False
