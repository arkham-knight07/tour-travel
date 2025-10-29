# TravelMate — New Features Setup Guide

This guide covers the new **Globe Explorer**, **Database**, and **Authentication** features added to your travel website.

---

## 🌍 **1. Globe Explorer Feature**

### What's New

- Interactive 3D globe where users can explore all destinations and treks
- Click or hover over place markers to see details
- Search destinations directly from the globe
- Zoom, pan, and auto-rotate controls
- Seamless integration with booking system

### Features

- **Static Place Data**: 11 places pre-loaded (5 domestic, 3 treks, 3 international)
- **Color-Coded Markers**:
  - 🔴 Red = Domestic Destinations
  - 🔵 Cyan = Treks
  - 🟡 Yellow = International
- **Interactive Details Panel**: Shows place name, category, description, price, coordinates
- **Search**: Find places by name
- **Navigation Links**: Click "Explore More" to go to the destination page

### How to Use

1. Click **"🌍 Globe"** in the navbar
2. Hover over any marker to see place details
3. Click a marker to pin the details panel
4. Use **+/−** buttons to zoom in/out
5. Click **⟲** to reset the globe
6. Search for a specific destination in the search bar

### Files Created

```
frontend/pages/globe.html          # Globe page UI
frontend/scripts/globe.js          # Globe.gl initialization and interactions
```

### Technology Stack

- **Globe.gl** (WebGL 3D globe) via CDN
- **Three.js** for 3D rendering
- Responsive design for mobile/desktop

---

## 🗄️ **2. Database Setup**

### Database Choice

Your project now uses **SQLite** for development (no extra setup needed) and supports **PostgreSQL** for production.

#### SQLite (Development) ✅

- **File**: `backend/travelmate.db` (auto-created on first run)
- **Pros**: Zero config, works locally, perfect for testing
- **No action needed**: It's automatic!

#### PostgreSQL (Production)

When ready to go live, just change `DATABASE_URL` in `.env`:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/travelmate
```

### Database Initialization

Run this command once to create the database and tables:

```bash
cd backend
source venv/bin/activate
python -m flask db upgrade
```

Or manually in Python:

```python
from config.database import Base, engine
Base.metadata.create_all(bind=engine)
```

### Database Models

#### **User Model** (`models/user.py`)

Stores user account information for authentication:

```
- id (Primary Key)
- name (User name)
- email (Unique, indexed)
- password_hash (Bcrypt hashed)
- phone (Optional)
- country (Default: India)
- is_active (Account status)
- created_at / updated_at (Timestamps)
```

#### **Place Model** (`models/place.py`)

Stores destination and place information for the globe:

```
- id (Primary Key)
- name (Place name)
- location_name (City/Region)
- latitude / longitude (Coordinates)
- description (Long text)
- category (destination, trek, international)
- image_url (Path to image)
- price (e.g., "₹8,999")
- is_featured (Boolean)
- rating / review_count (Optional)
- created_at / updated_at (Timestamps)
```

### Existing Data Not Changed

- All existing JSON files (tours.json, faq.json, bookings.json) work as-is
- Database is purely additive — no breaking changes
- Tours, bookings, and chatbot operate independently

---

## 🔐 **3. Authentication System**

### New Auth Routes (No Breaking Changes)

All new routes are under `/api/auth/` and don't affect existing APIs.

#### Endpoints

**Register a New User**

```bash
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "secure_password",
  "phone": "+91-9999999999",
  "country": "India"
}

Response (201 Created):
{
  "message": "User registered successfully",
  "user": { "id": 1, "name": "John Doe", "email": "john@example.com", ... },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Login User**

```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "secure_password"
}

Response (200 OK):
{
  "message": "Login successful",
  "user": { ... },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Get Current User Profile**

```bash
GET /api/auth/me
Authorization: Bearer <token>
Or Cookie: auth_token=<token>

Response (200 OK):
{
  "user": { "id": 1, "name": "John Doe", ... }
}
```

**Update User Profile**

```bash
PUT /api/auth/update
Content-Type: application/json
Authorization: Bearer <token>

{
  "name": "Jane Doe",
  "phone": "+91-8888888888",
  "country": "USA"
}

Response (200 OK):
{
  "message": "Profile updated successfully",
  "user": { ... }
}
```

**Logout**

```bash
POST /api/auth/logout

Response (200 OK):
{
  "message": "Logout successful"
}
```

### Token Management

- **JWT Tokens** (JSON Web Tokens) generated on login/register
- **Token Storage**: HttpOnly cookies (secure + recommended) or localStorage
- **Token Expiry**: 24 hours (configurable in `.env`)
- **Refresh**: Create new token on each login

---

## 📍 **4. Places API** (For Globe Data)

### Endpoints

**Get All Places**

```bash
GET /api/places?category=destination&featured=true&page=1&limit=10

Query Parameters:
- category: 'destination', 'trek', 'international' (optional)
- featured: 'true' to show only featured (optional)
- page: Page number (default: 1)
- limit: Items per page (default: 20)

Response:
{
  "places": [ { "id": 1, "name": "Goa, India", ... }, ... ],
  "total": 11,
  "page": 1,
  "limit": 20,
  "pages": 1
}
```

**Get Single Place**

```bash
GET /api/places/1

Response:
{
  "place": { "id": 1, "name": "Goa, India", "latitude": 15.2993, ... }
}
```

**Search Places**

```bash
GET /api/places/search?q=Goa

Query Parameters:
- q: Search term (min 2 characters)

Response:
{
  "results": [ { "id": 1, "name": "Goa, India", ... } ],
  "count": 1
}
```

**Create New Place** (Admin only in production)

```bash
POST /api/places
Content-Type: application/json

{
  "name": "Shimla, India",
  "location_name": "Himachal Pradesh",
  "latitude": 31.7846,
  "longitude": 77.1066,
  "description": "Beautiful hill station...",
  "category": "destination",
  "image_url": "assets/images/destinations/shimla.jpg",
  "price": "₹9,999",
  "is_featured": true,
  "rating": 4.5
}

Response (201 Created):
{
  "message": "Place created successfully",
  "place": { ... }
}
```

---

## 🚀 **Starting the Servers**

### Backend (Port 5001)

```bash
cd backend
source venv/bin/activate
python app.py
```

Output:

```
✅ Database initialized: sqlite:///./travelmate.db
 * Running on http://127.0.0.1:5001
```

### Frontend (Port 8000)

```bash
cd frontend
python3 -m http.server 8000
```

Then open: **http://localhost:8000**

---

## 📝 **Environment Variables** (`.env`)

```bash
# Existing
GEMINI_API_KEY=AIzaSyBc9Ib_NAoNKStT21bXho7pqD5qIw1Syy4
USE_FALLBACK=true

# New: Database
DATABASE_URL=sqlite:///./travelmate.db
# For PostgreSQL: postgresql://user:password@localhost:5432/travelmate

# New: Authentication
JWT_SECRET=travelmate-secret-key-change-in-production-2024
# Change this to a random string in production!
```

---

## 🔄 **How It All Works Together**

```
┌─────────────────────────────────────────────────────────────┐
│                     User Browser                            │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Login/Register (pages/login.html)                   │  │
│  │ ↓                                                     │  │
│  │ POST /api/auth/register → JWT Token                │  │
│  │ POST /api/auth/login → JWT Token + HttpOnly Cookie  │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Globe Explorer (pages/globe.html)                    │  │
│  │ GET /api/places → Display 11 places on 3D globe     │  │
│  │ Click marker → Show details + "Explore More" link   │  │
│  │ Redirect to destinations.html                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                          ↓                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Browse & Book (existing features)                    │  │
│  │ - Destinations page                                   │  │
│  │ - Search & filter                                     │  │
│  │ - Chatbot (AI-powered)                                │  │
│  │ - Booking system                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
              ↓ (Backend API)
┌─────────────────────────────────────────────────────────────┐
│               Flask Backend (Port 5001)                     │
│                                                              │
│  ✅ Existing APIs (Untouched):                              │
│  - GET /api/tours → Tours from tours.json                  │
│  - POST /api/bookings → Store bookings                     │
│  - POST /chat → AI chatbot (Gemini)                        │
│                                                              │
│  ✨ New APIs:                                              │
│  - /api/auth/* → User authentication & profile             │
│  - /api/places/* → Places/destinations for globe           │
│                                                              │
│  📊 Database (SQLite/PostgreSQL):                          │
│  - Users table                                              │
│  - Places table                                             │
│  - (Bookings, Tours can be migrated later if needed)       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔮 **Next Steps (Login Page)**

Currently, the globe shows static place data. To add the **Login page**:

1. Create `frontend/pages/login.html` with registration/login forms
2. Create `frontend/scripts/auth.js` to handle form submissions + JWT storage
3. Update navbar to show user profile when logged in
4. Store JWT token securely (HttpOnly cookie)
5. Protect routes that require authentication

**Would you like me to build the Login page next?**

---

## ✅ **What's Not Changed**

- ✅ Existing HTML pages (index, destinations, booking, etc.)
- ✅ Tours JSON data (tours.json still works)
- ✅ Chatbot functionality (still uses Gemini AI)
- ✅ Booking system (stores in bookings.json by default)
- ✅ FAQ & search features
- ✅ CSS styling and responsive design

Everything is **purely additive** — no breaking changes!

---

## 🐛 **Troubleshooting**

**Issue**: `ModuleNotFoundError: No module named 'sqlalchemy'`  
**Fix**: Run `pip install -r requirements.txt` in the backend venv

**Issue**: Globe page shows blank  
**Fix**: Ensure Globe.gl CDN is reachable (needs internet); check browser console for errors

**Issue**: Auth endpoints return 404  
**Fix**: Restart backend server (`python app.py`)

**Issue**: CORS errors when calling API  
**Fix**: Already configured with `CORS(app)` in app.py

---

## 📞 **Support**

If you hit any issues:

1. Check the browser console for errors (`F12` → Console tab)
2. Check backend logs (terminal where `python app.py` runs)
3. Verify `.env` variables are set
4. Ensure ports 8000 (frontend) and 5001 (backend) are free

---

**You're all set! 🚀 Enjoy your enhanced travel platform!**
