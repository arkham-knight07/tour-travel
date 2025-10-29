import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

from utils.jsonstore import load_json_any

# Load fallback FAQ for when AI fails
FAQ = load_json_any("data/faq.json")

# Configure Gemini AI
def configure_gemini():
    """Configure Gemini AI with API key"""
    if not GENAI_AVAILABLE:
        return False
        
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("⚠️  Warning: GEMINI_API_KEY not found in environment variables")
            return False
        
        genai.configure(api_key=api_key)
        print("✅ Gemini AI configured successfully")
        return True
    except Exception as e:
        print(f"❌ Gemini configuration error: {e}")
        return False

# Travel-specific AI prompt
TRAVEL_SYSTEM_PROMPT = """You are a helpful travel assistant for TravelMate, a travel booking platform. 

About TravelMate:
- We offer flights, hotels, buses, trains, treks, and international trips
- Popular destinations: Goa, Manali, Kerala, Ladakh, Jaipur, Bali, Paris, New York
- Services include booking, visa assistance, 24/7 support
- Contact: support@travelmate.com, +91-9876543210

Key Information:
- Booking: Go to any package and click "Book", fill details and confirm
- Payment: We accept UPI, cards, and PayPal with email invoices
- Refunds: Processed within 5-7 business days after approval
- Cancellation: Full refund if cancelled 7+ days before departure
- Visa: International packages include visa guidance and documents
- Popular treks: Everest Base Camp (₹45,999), Hampta Pass (₹12,999), Sandakphu (₹15,999)

Guidelines:
- Keep responses helpful, friendly, and travel-focused
- If asked about specific destinations, suggest our packages
- For booking help, guide users to the booking page
- Be concise but informative (2-3 sentences max)
- Use emojis occasionally for friendliness
- If unsure, ask for clarification or suggest contacting support

User Question: """

def reply_to(message: str) -> str:
    """Generate AI response using Gemini or fallback to FAQ"""
    msg = (message or "").strip()
    if not msg:
        return "Hi! 👋 I'm your TravelMate assistant. Ask me about booking, destinations, payments, or any travel questions!"

    # Try Gemini AI first
    if configure_gemini():
        try:
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            response = model.generate_content(TRAVEL_SYSTEM_PROMPT + msg)
            
            if response and hasattr(response, 'text') and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini AI error: {e}")
            # Fall back to FAQ system
    
    # Fallback to original FAQ system
    return fallback_reply(msg)

def fallback_reply(message: str) -> str:
    """Fallback FAQ system when AI is unavailable"""
    msg = message.lower().strip()
    
    # Exact keyword match first
    for key, ans in FAQ.items():
        if key.lower() in msg:
            return ans + " 🌟"

    # Fuzzy matching
    words = set(w.strip(".,!?") for w in msg.split())
    best_key, best_score = None, 0
    for key in FAQ:
        score = len(words.intersection(set(key.lower().split())))
        if score > best_score:
            best_key, best_score = key, score
    
    if best_key:
        return FAQ[best_key] + " ✨"

    return "I can help with booking, destinations, payment, refunds, cancellation, or visa questions. What would you like to know? 🤔"
