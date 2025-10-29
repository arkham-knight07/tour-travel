# 🔐 Login & Globe Features — Quick Guide

## ✅ What's New

### 1. **🔐 Login Page** ✨ NEW

- **Location**: `pages/login.html`
- **Features**:
  - ✅ Sign In (existing users)
  - ✅ Sign Up (new users)
  - ✅ Remember me option
  - ✅ Forgot password link
  - ✅ Social login buttons (Google, GitHub, Apple)
  - ✅ Real-time validation
  - ✅ Error messages
  - ✅ Success notifications

### 2. **🌍 Globe Page** ✨ FIXED

- **Location**: `pages/globe.html`
- **Features**:
  - ✅ 3D interactive globe
  - ✅ Live data from MongoDB API
  - ✅ 15+ destinations & treks
  - ✅ Place search
  - ✅ Hover to see details
  - ✅ Click for more info
  - ✅ Zoom controls
  - ✅ Auto-rotation

---

## 🚀 How to Use

### **Access Login Page**

1. Go to: `http://localhost:8000`
2. Click **🔐 Login** button in navbar
3. OR go directly to: `http://localhost:8000/pages/login.html`

### **Create New Account (Sign Up)**

1. Click **Sign Up** at bottom of login form
2. Fill in:

   - Full Name
   - Email
   - Phone
   - Country
   - Password (min 6 chars)
   - Confirm Password

3. Click **Create Account**
4. ✅ Success! Redirected to home page

### **Login**

1. Enter your email
2. Enter your password
3. Check "Remember me" (optional)
4. Click **Sign In**
5. ✅ Success! Redirected to home page

### **Access Globe**

1. Go to: `http://localhost:8000`
2. Click **🌍 Globe** in navbar
3. OR go directly to: `http://localhost:8000/pages/globe.html`

### **Use Globe**

- **Hover** over markers to see place details
- **Click** on markers to select a place
- **Search** for destinations by name
- **Zoom** in/out with + and − buttons
- **Reset** to see full globe
- **View** place info in the bottom-right panel
- **Click** "Explore More" to go to destination page

---

## 📍 Places on Globe

### **Domestic Destinations** 🇮🇳

- Goa (beach paradise)
- Manali (mountain adventure)
- Kerala (backwaters)
- Ladakh (high desert)
- Jaipur (pink city)

### **Treks** 🏔️

- Everest Base Camp
- Hampta Pass
- Sandakphu

### **International** 🌎

- Bali, Indonesia
- Paris, France
- New York, USA

---

## 📊 API Integration

### **Backend Endpoints Used**

```bash
# Register new user
POST /api/auth/register
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "1234567890",
  "country": "USA"
}

# Login user
POST /api/auth/login
{
  "email": "john@example.com",
  "password": "password123"
}

# Get all places for globe
GET /api/places?limit=100
```

### **Response Example**

```json
{
  "places": [
    {
      "id": "goa",
      "name": "Goa, India",
      "latitude": 15.2993,
      "longitude": 73.8243,
      "description": "Beautiful beaches...",
      "category": "destination",
      "image_url": "...",
      "price": 8999,
      "rating": 4.5,
      "review_count": 128
    }
  ]
}
```

---

## 🔧 Technical Details

### **Login Page Architecture**

```
login.html (form UI)
    ↓
JavaScript event handler
    ↓
API call to backend
    ↓
Token stored in localStorage
    ↓
User redirected to home
```

### **Globe Page Architecture**

```
globe.html (UI)
    ↓
globe.js (initialization)
    ↓
loadPlacesFromAPI() function
    ↓
Fetch from /api/places
    ↓
Create 3D globe with Three.js
    ↓
Display interactive markers
```

---

## 🐛 Troubleshooting

### **"API Error" when loading globe**

**Problem**: Globe not loading places from API

**Solution**:

1. Check backend is running on port 5002

   ```bash
   curl http://localhost:5002/health
   ```

2. Check API returns data

   ```bash
   curl http://localhost:5002/api/places
   ```

3. Verify globe.js has correct URL:
   ```javascript
   const API_BASE_URL = "http://localhost:5002"; // Should be 5002, not 5001
   ```

### **Login fails with "Invalid credentials"**

**Problem**: Can't login

**Solution**:

1. Make sure you registered an account first
2. Check email is correct
3. Check password is correct (case-sensitive)
4. Try registering a new account

### **Login form not submitting**

**Problem**: Form freezes when clicking submit

**Solution**:

1. Check backend is running
2. Check MongoDB is running
3. Check browser console for errors (F12)
4. Try refreshing page

---

## ✨ Features Roadmap

### **Coming Soon**

- [ ] User profile page
- [ ] Edit profile
- [ ] Logout functionality
- [ ] Password reset
- [ ] Email verification
- [ ] Two-factor authentication
- [ ] Social login integration
- [ ] Wishlist feature
- [ ] Booking history
- [ ] User reviews & ratings

---

## 📝 Test Credentials

You can create your own account by signing up, or test with:

```
Email: test@example.com
Password: password123
```

(Create this account by signing up first)

---

## 🎯 Next Steps

1. ✅ Open http://localhost:8000
2. ✅ Create an account (Sign Up)
3. ✅ Login with your credentials
4. ✅ Click 🌍 Globe to see interactive globe
5. ✅ Search for places and click markers
6. ✅ Explore destinations

---

## 📞 Support

If you encounter any issues:

1. **Check logs** - Open browser console (F12)
2. **Check backend** - Verify http://localhost:5002 is running
3. **Check MongoDB** - Verify MongoDB is running
4. **Restart services** - Kill and restart backend/frontend

```bash
# Restart backend
CTRL+C in backend terminal
python app.py

# Restart frontend
CTRL+C in frontend terminal
python3 -m http.server 8000
```

---

## 🎉 You're All Set!

Everything is ready to use. Go explore! 🌍

- Home: http://localhost:8000
- Login: http://localhost:8000/pages/login.html
- Globe: http://localhost:8000/pages/globe.html

**Happy traveling! ✈️**
