# 🚨 DEPLOYMENT CHECKLIST

Before deploying to GitHub and Vercel, complete these steps:

## ✅ Pre-Deployment Checklist

### 1. Security

- [ ] Remove `.env` file from git (should be in `.gitignore`)
- [ ] Verify no API keys are hardcoded in source files
- [ ] Generate strong JWT_SECRET for production
- [ ] Enable HTTPS cookies (`secure=True` in auth_routes.py)

### 2. Database

- [ ] Create MongoDB Atlas account (free tier available)
- [ ] Get production MongoDB connection string
- [ ] Update MONGODB_URI in environment variables
- [ ] Test database connection

### 3. API Keys

- [ ] Get Google Gemini API key from https://makersuite.google.com/app/apikey
- [ ] Add GEMINI_API_KEY to environment variables

### 4. Configuration Files

- [x] `.gitignore` created
- [x] `README.md` created
- [x] `.env.example` created
- [x] `vercel.json` files created

### 5. Code Updates

- [ ] Update API base URL in `frontend/scripts/api.js` for production
- [ ] Update CORS settings in `backend/app.py` for production domain
- [ ] Set `secure=True` for cookies in production

### 6. Testing

- [ ] Test all major features locally
- [ ] Test login/signup flow
- [ ] Test booking creation
- [ ] Test chatbot responses
- [ ] Test globe visualization

## 🔐 Setup MongoDB Atlas (Free Production Database)

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Create a free account
3. Create a new cluster (M0 Free tier)
4. Database Access → Add New Database User
5. Network Access → Add IP Address (0.0.0.0/0 for testing, restrict later)
6. Click "Connect" → "Connect your application"
7. Copy connection string: `mongodb+srv://<username>:<password>@cluster.mongodb.net/travelmate`

## 📦 Deploy to GitHub

```bash
# Initialize git (if not already done)
cd /Users/shresthaverdhan/Desktop/PROJECT/tour-travel
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: TravelMate travel booking platform"

# Create GitHub repository at https://github.com/new
# Then link and push:
git remote add origin https://github.com/YOUR_USERNAME/tour-travel.git
git branch -M main
git push -u origin main
```

## 🚀 Deploy to Vercel

### Frontend Deployment

1. Install Vercel CLI:

```bash
npm i -g vercel
```

2. Deploy frontend:

```bash
cd frontend
vercel --prod
```

3. Note the deployment URL (e.g., `https://tour-travel.vercel.app`)

### Backend Deployment

1. Deploy backend:

```bash
cd ../backend
vercel --prod
```

2. Add environment variables in Vercel dashboard:

   - Go to your project → Settings → Environment Variables
   - Add:
     - `MONGODB_URI`: Your MongoDB Atlas connection string
     - `JWT_SECRET`: A secure random string
     - `GEMINI_API_KEY`: Your Google Gemini API key
     - `FLASK_ENV`: production
     - `DEBUG`: False

3. Note the backend URL (e.g., `https://tour-travel-api.vercel.app`)

### Update Frontend API URL

1. Edit `frontend/scripts/api.js`:

```javascript
const API_BASE = "https://tour-travel-api.vercel.app"; // Your backend URL
```

2. Redeploy frontend:

```bash
cd frontend
vercel --prod
```

## 🔄 Alternative: Deploy Both Together

Create a monorepo vercel.json in root:

```json
{
  "builds": [
    { "src": "frontend/**", "use": "@vercel/static" },
    { "src": "backend/app.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "backend/app.py" },
    { "src": "/(.*)", "dest": "frontend/$1" }
  ]
}
```

## ✅ Post-Deployment

1. Test the live site thoroughly
2. Check browser console for errors
3. Test all API endpoints
4. Verify MongoDB connection
5. Test chatbot with AI
6. Share your live URL! 🎉

## 🌐 Your URLs

After deployment, you'll have:

- Frontend: `https://your-project.vercel.app`
- Backend API: `https://your-project-api.vercel.app`
- MongoDB: Atlas cloud database

## 📝 Notes

- Vercel free tier includes:
  - Unlimited deployments
  - Automatic HTTPS
  - CDN
  - Serverless functions
- MongoDB Atlas free tier includes:
  - 512 MB storage
  - Shared RAM
  - Perfect for small projects

## 🆘 Common Issues

**Issue**: Module not found
**Fix**: Add missing packages to `requirements.txt`

**Issue**: Database connection failed
**Fix**: Check MongoDB Atlas IP whitelist and connection string

**Issue**: CORS errors
**Fix**: Update CORS settings in `app.py` with your frontend domain

**Issue**: API key errors
**Fix**: Verify environment variables are set in Vercel dashboard

---

✨ **You're ready to deploy!** Follow the steps above and your project will be live!
