# 🌍 TravelMate - Travel Booking Platform

A full-stack travel booking platform featuring flights, hotels, treks, and international trips with an AI-powered chatbot and interactive 3D globe visualization.

## ✨ Features

- 🎫 **Multi-Service Booking**: Flights, hotels, buses, trains, treks, and international packages
- 🤖 **AI Chatbot**: Gemini AI-powered support assistant
- 🌐 **Interactive Globe**: 3D visualization of destinations using Globe.gl
- 🔐 **User Authentication**: JWT-based login/signup with MongoDB
- 📱 **PWA Support**: Install as a mobile app
- 🎨 **Modern UI**: Dark theme with smooth animations
- 💳 **Booking Management**: Track and manage bookings
- ⭐ **Reviews & Ratings**: Customer feedback system

## 🛠️ Tech Stack

### Frontend

- HTML5, CSS3, JavaScript (ES6+)
- Globe.gl (3D visualization)
- PWA (Progressive Web App)
- Responsive design

### Backend

- Python 3.x
- Flask (Web framework)
- MongoDB (Database)
- MongoEngine (ODM)
- Google Gemini AI (Chatbot)
- JWT (Authentication)

## 📋 Prerequisites

- Python 3.8+
- MongoDB 4.4+
- Google Gemini API Key
- Modern web browser

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/arkham-knight07/tour-travel.git
cd tour-travel
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/travelmate

# JWT Configuration
JWT_SECRET=your-secret-key-change-this-in-production

# Google Gemini API
GEMINI_API_KEY=your-gemini-api-key-here

# Flask Configuration
FLASK_ENV=development
DEBUG=True
EOF

# Start MongoDB (macOS)
brew services start mongodb-community

# Run the backend server
python app.py
```

The backend will start at `http://127.0.0.1:5002`

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Serve the frontend (using Python's HTTP server)
python3 -m http.server 8000
```

The frontend will be available at `http://localhost:8000`

## 📁 Project Structure

```
tour-travel/
├── frontend/
│   ├── index.html              # Homepage
│   ├── manifest.json            # PWA manifest
│   ├── service-worker.js        # Service worker for PWA
│   ├── pages/                   # HTML pages
│   │   ├── booking.html
│   │   ├── login.html
│   │   ├── globe.html
│   │   └── ...
│   ├── scripts/                 # JavaScript modules
│   │   ├── api.js
│   │   ├── chatbot.js
│   │   ├── globe.js
│   │   └── main.js
│   ├── styles/                  # CSS files
│   ├── assets/                  # Images, videos, icons
│   └── data/                    # Static JSON data
│
└── backend/
    ├── app.py                   # Flask application entry point
    ├── requirements.txt         # Python dependencies
    ├── api/                     # API route blueprints
    │   ├── auth_routes.py       # Authentication endpoints
    │   ├── places_routes.py     # Places/destinations CRUD
    │   ├── booking_routes.py    # Booking management
    │   ├── chatbot_routes.py    # AI chatbot
    │   └── tours_routes.py      # Tour packages
    ├── models/                  # MongoDB models
    │   ├── user.py
    │   ├── place.py
    │   └── booking.py
    ├── services/                # Business logic
    │   ├── chatbot_service.py
    │   ├── booking_service.py
    │   └── tour_service.py
    ├── config/                  # Configuration
    │   └── database.py
    └── utils/                   # Helper functions
```

## 🔧 API Endpoints

### Authentication

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user profile
- `POST /api/auth/logout` - Logout user
- `PUT /api/auth/update` - Update user profile

### Places

- `GET /api/places` - Get all places (with filters)
- `GET /api/places/<id>` - Get specific place
- `GET /api/places/search?q=<query>` - Search places
- `POST /api/places` - Create new place
- `PUT /api/places/<id>` - Update place
- `DELETE /api/places/<id>` - Delete place

### Bookings

- `GET /api/bookings` - Get all bookings
- `POST /api/bookings` - Create new booking

### Chatbot

- `POST /chat` - Send message to AI chatbot
- `GET /chat/faq` - Get FAQ data

### Tours

- `GET /api/tours` - Get tour packages

## 🔑 Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
MONGODB_URI=mongodb://localhost:27017/travelmate

# JWT Authentication
JWT_SECRET=your-super-secret-jwt-key-change-this

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Flask
FLASK_ENV=development
DEBUG=True
```

## 🌐 Deployment

### Deploy to Vercel (Frontend)

1. Install Vercel CLI:

```bash
npm i -g vercel
```

2. Deploy frontend:

```bash
cd frontend
vercel
```

### Deploy Backend (Options)

**Option 1: Railway/Render**

- Push code to GitHub
- Connect repository to Railway/Render
- Add environment variables
- Deploy

**Option 2: Heroku**

```bash
cd backend
heroku create your-app-name
git push heroku main
```

**Important**: Update API URLs in frontend after deploying backend!

## 📝 Configuration for Production

1. **Update API URLs** in `frontend/scripts/api.js`:

   ```javascript
   const API_BASE = "https://your-backend-url.com";
   ```

2. **Set MongoDB Atlas URL** in backend `.env`:

   ```env
   MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/travelmate
   ```

3. **Enable HTTPS** cookies in `backend/api/auth_routes.py`:

   ```python
   secure=True  # Change from False
   ```

4. **Update CORS** in `backend/app.py` for your domain

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest
```

### Test API Endpoints

```bash
# Health check
curl http://127.0.0.1:5002/health

# Get places
curl http://127.0.0.1:5002/api/places
```

## 🐛 Troubleshooting

### MongoDB Connection Error

```bash
# Start MongoDB
brew services start mongodb-community  # macOS
sudo systemctl start mongod            # Linux
```

### Port Already in Use

```bash
# Kill process on port 5002
lsof -ti:5002 | xargs kill -9

# Or use a different port in app.py
```
### Screenshots

1. Main Page
   <img width="1464" height="802" alt="Screenshot 2025-10-29 at 12 30 37 PM" src="https://github.com/user-attachments/assets/128939ca-067a-419a-96b7-decd99ddbde4" />

2.Destination Page
<img width="716" height="754" alt="Screenshot 2025-09-08 at 11 14 44 AM" src="https://github.com/user-attachments/assets/1d6522d2-faa5-4495-8e32-7bb23cb198da" />

3.Deal Page 
<img width="1459" height="812" alt="Screenshot 2025-10-29 at 12 30 50 PM" src="https://github.com/user-attachments/assets/0773205d-3330-4065-b66d-8ebc47278ba3" />

4.Globe Page
<img width="1448" height="752" alt="Screenshot 2025-11-09 at 10 24 00 AM" src="https://github.com/user-attachments/assets/f8692553-a066-499d-8783-57228914dd5e" />




### CORS Issues

- Check backend CORS configuration
- Ensure frontend is making requests to correct backend URL

## 📄 License

MIT License - feel free to use this project for learning or commercial purposes.

## 👨‍💻 Author

Created with ❤️ by [arkham-knight07](https://github.com/arkham-knight07) ,[rayak25](https://github.com/rayak25) ,[Nav2428](https://github.com/Nav2428)

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first.

## 📞 Support

For support, email verdhanchiku@gmail.com or open an issue.

---

**Happy Traveling! ✈️🌍**
