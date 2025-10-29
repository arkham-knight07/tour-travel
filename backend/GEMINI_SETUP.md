# 🤖 Setting up Gemini AI for TravelMate Chatbot

## Step 1: Get Your Free Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

## Step 2: Add API Key to Your Project

1. Open the file `backend/.env`
2. Replace `your-gemini-api-key-here` with your actual API key:
   ```
   GEMINI_API_KEY=AIzaSy...your-actual-key-here
   ```

## Step 3: Restart Your Backend Server

1. Stop the current backend server (Ctrl+C)
2. Restart it:
   ```bash
   cd backend
   source venv/bin/activate  # if using virtual environment
   python app.py
   ```

## Step 4: Test Your AI Chatbot

1. Open your website at http://localhost:8000
2. Click the chat button (orange pulsing button)
3. Ask complex questions like:
   - "What's the best time to visit Goa?"
   - "I want a romantic trip for 2 people to Paris"
   - "Tell me about trekking options in the Himalayas"

## Features of Your New AI Chatbot

✅ **Natural Language Understanding** - Understands complex questions
✅ **Travel Expertise** - Knows about destinations, bookings, and travel
✅ **Personalized Responses** - Tailored to your TravelMate business
✅ **Fallback System** - Uses FAQ if AI is unavailable
✅ **Free Tier** - Generous free usage limits

## Troubleshooting

- **"Server unavailable"**: Check if API key is correct in .env file
- **Slow responses**: Gemini API might be busy, try again
- **Error messages**: Backend will fall back to FAQ system automatically

Your chatbot is now powered by Google Gemini AI! 🚀
