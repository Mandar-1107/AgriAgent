# app.py - AgriAgent with Fixed Weather & Modern UI
import streamlit as st
import google.generativeai as genai
import requests
from datetime import datetime
from PIL import Image
from typing import Optional, Dict, Any, List
import re
from config import *

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="AgriAgent - AI Agriculture Assistant",
    page_icon="🌾",
    
    
)

# ==================== MODERN CHATBOT UI ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', sans-serif;
    }
    
    /* Dark background */
    .main {
        background: #0f1419;
        min-height: 100vh;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Chat container */
    .chat-container {
        max-width: 850px;
        margin: 0 auto;
        padding: 100px 20px 160px 20px;
        
    }
    
    /* Welcome message */
    .welcome-message {
        text-align: center;
        padding: 40px 20px;
        color: #8b98a5;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .welcome-message h2 {
        color: #fff;
        font-size: 1.8em;
        margin-bottom: 12px;
    }
    
    /* Message bubbles */
    .message-container {
        display: flex;
        margin-bottom: 16px;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .message-bubble {
        max-width: 75%;
        padding: 12px 16px;
        border-radius: 16px;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 15px;
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: #fff;
        border-radius: 16px 16px 2px 16px;
    }
    
    .assistant-bubble {
        background: #1c2128;
        color: #e6edf3;
        border-radius: 16px 16px 16px 2px;
        border: 1px solid #30363d;
    }
    
    /* Input area */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #0f1419;
        padding: 16px 20px 20px 20px;
        border-top: 1px solid #30363d;
        z-index: 1000;
    }
    
    .input-wrapper {
        max-width: 850px;
        margin: 0 auto;
        display: flex;
        gap: 10px;
        align-items: center;
        position: relative;
    }
    
    /* Text input */
    .stTextInput {
        flex: 1;
    }
    
    .stTextInput > div > div > input {
        border-radius: 24px !important;
        padding: 13px 90px 13px 20px !important;
        border: 1px solid #30363d !important;
        font-size: 15px !important;
        background: #1c2128 !important;
        color: #e6edf3 !important;
        transition: all 0.2s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #8b98a5 !important;
    }
    
    /* Upload button styling */
    .upload-btn {
        position: absolute;
        right: 65px;
        top: 50%;
        transform: translateY(-50%);
        background: transparent;
        border: none;
        color: #8b98a5;
        font-size: 20px;
        cursor: pointer;
        padding: 6px;
        border-radius: 8px;
        transition: all 0.2s;
        z-index: 10;
    }
    
    .upload-btn:hover {
        color: #667eea;
        background: rgba(102, 126, 234, 0.1);
    }
    
    /* Hide file uploader visuals */
    [data-testid="stFileUploader"] {
        position: absolute;
        right: 60px;
        top: 0;
        width: 40px;
        height: 48px;
        opacity: 0;
        cursor: pointer;
    }
    
    [data-testid="stFileUploader"] section {
        display: none;
    }
    
    /* Clear button */
    .stButton > button {
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        padding: 0 !important;
        font-size: 16px !important;
        border: 1px solid #30363d !important;
        background: #1c2128 !important;
        color: #8b98a5 !important;
        transition: all 0.2s !important;
    }
    
    .stButton > button:hover {
        background: #21262d !important;
        border-color: #484f58 !important;
        color: #e6edf3 !important;
    }
    
    /* Upload badge */
    .upload-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 12px;
        background: #667eea;
        color: white;
        border-radius: 12px;
        font-size: 13px;
        font-weight: 500;
        margin-top: 8px;
    }
    
    /* Hide streamlit */
    #MainMenu, footer, header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    
    /* Responsive */
    @media (max-width: 768px) {
        .message-bubble {
            max-width: 85%;
        }
        .chat-container {
            padding: 90px 12px 150px 12px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==================== SESSION STATE ====================
def initialize_session_state():
    defaults = {
        "messages": [],
        "weather_data": None,
        "weather_cache_time": None,
        "last_location": None,
        "processed_input": None,
        "input_counter": 0,
        "context": {
            "location": None,
            "soil_type": None,
            "water_source": None,
            "budget": None,
            "experience": None,
            "farm_size": None
        }
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

# ==================== API CONFIGURATION ====================
def configure_gemini():
    if not GEMINI_API_KEY:
        st.error("⚠️ Gemini API Key Missing")
        st.stop()
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        st.stop()

configure_gemini()

# ==================== HELPER FUNCTIONS ====================
def get_indian_season() -> str:
    month = datetime.now().month
    for season, months in INDIAN_SEASONS.items():
        if month in months:
            return season
    return "Transition Period"

def extract_context_from_history():
    context = st.session_state.context.copy()
    
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            content_lower = msg["content"].lower()
            
            # Expanded location detection
            location_keywords = ["maharashtra", "punjab", "karnataka", "gujarat", "rajasthan", 
                               "mp", "up", "bihar", "jammu", "kashmir", "j&k", "jk", "amravati", 
                               "mumbai", "pune", "srinagar", "jammu city", "delhi", "bangalore"]
            
            if not context["location"]:
                for keyword in location_keywords:
                    if keyword in content_lower:
                        context["location"] = msg["content"]
                        break
            
            if not context["soil_type"] and any(word in content_lower for word in ["clay", "sand", "loam", "soil"]):
                context["soil_type"] = msg["content"]
            
            if not context["water_source"] and any(word in content_lower for word in ["rain", "irrigation", "well", "canal"]):
                context["water_source"] = msg["content"]
            
            if not context["budget"] and any(word in content_lower for word in ["budget", "money", "lakh", "investment"]):
                context["budget"] = msg["content"]
            
            if not context["farm_size"] and any(word in content_lower for word in ["acre", "hectare"]):
                context["farm_size"] = msg["content"]
            
            if not context["experience"] and any(word in content_lower for word in ["beginner", "new", "experienced"]):
                context["experience"] = msg["content"]
    
    st.session_state.context = context
    return context

def is_simple_greeting(message: str) -> bool:
    greetings = ['hi', 'hello', 'hey', 'namaste', 'namaskar']
    casual = ['how are you', 'what is your name', 'who are you']
    
    message_lower = message.lower().strip()
    
    if message_lower in greetings or any(phrase in message_lower for phrase in casual):
        if len(message_lower) < 30:
            return True
    
    return False

def remove_markdown_formatting(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    return text

def extract_location_from_query(query: str) -> Optional[str]:
    """Extract city/state name with better matching for states like J&K"""
    # City-level locations
    cities = ["mumbai", "delhi", "bangalore", "hyderabad", "chennai", "kolkata", "pune", 
              "ahmedabad", "jaipur", "lucknow", "nagpur", "indore", "bhopal", "patna", 
              "amravati", "nashik", "aurangabad", "solapur", "srinagar", "jammu"]
    
    # State-level locations (will use capital city)
    states_to_cities = {
        "maharashtra": "mumbai",
        "punjab": "chandigarh",
        "karnataka": "bangalore",
        "gujarat": "ahmedabad",
        "rajasthan": "jaipur",
        "mp": "bhopal",
        "madhya pradesh": "bhopal",
        "up": "lucknow",
        "uttar pradesh": "lucknow",
        "bihar": "patna",
        "jammu": "jammu",
        "kashmir": "srinagar",
        "j&k": "srinagar",
        "jk": "srinagar",
        "jammu and kashmir": "srinagar",
        "jammu kashmir": "srinagar"
    }
    
    query_lower = query.lower()
    
    # Check for cities first
    for city in cities:
        if city in query_lower:
            return city.title()
    
    # Check for states and return capital
    for state, capital in states_to_cities.items():
        if state in query_lower:
            return capital.title()
    
    return None

def get_weather_data(location: str) -> Optional[Dict[str, Any]]:
    """Improved weather fetching with better error handling"""
    if not WEATHER_API_KEY:
        return None
    
    # Check cache
    if (st.session_state.weather_data and 
        st.session_state.last_location and
        st.session_state.last_location.lower() == location.lower() and
        st.session_state.weather_cache_time and
        (datetime.now() - st.session_state.weather_cache_time).seconds < WEATHER_CACHE_DURATION):
        return st.session_state.weather_data
    
    try:
        # Try with India country code for better results
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": f"{location},IN",  # Add India country code
            "appid": WEATHER_API_KEY,
            "units": WEATHER_UNITS
        }
        
        response = requests.get(url, params=params, timeout=WEATHER_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.weather_data = data
            st.session_state.weather_cache_time = datetime.now()
            st.session_state.last_location = location
            return data
        else:
            # Try without country code
            params = {"q": location, "appid": WEATHER_API_KEY, "units": WEATHER_UNITS}
            response = requests.get(url, params=params, timeout=WEATHER_TIMEOUT)
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.weather_data = data
                st.session_state.weather_cache_time = datetime.now()
                st.session_state.last_location = location
                return data
    except Exception as e:
        print(f"Weather API error: {e}")
    
    return None

def format_weather_context(weather_data: Dict[str, Any]) -> str:
    if not weather_data:
        return ""
    
    try:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        
        context = f"Weather in {weather_data['name']}: {temp}°C, {humidity}% humidity, {description}, wind {wind_speed} m/s."
        
        if temp > 35:
            context += " High heat - extra irrigation recommended."
        elif temp < 10:
            context += " Cold - frost protection needed."
        
        if humidity > 80:
            context += " High humidity - disease risk."
        elif humidity < 30:
            context += " Low humidity - increase irrigation."
        
        return context
    except:
        return ""

def resize_image(image: Image.Image, max_size: int = 2048) -> Image.Image:
    if max(image.size) > max_size:
        image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
    return image

def analyze_images_with_gemini(images: List[Image.Image], query: str = "") -> str:
    try:
        model = genai.GenerativeModel(GEMINI_VISION_MODEL)
        season = get_indian_season()
        
        prompt = f"""You are AgriAgent, agricultural expert.

Season: {season}
Query: "{query}"

Analyze {"these images" if len(images) > 1 else "this image"}:

1. Identification: What crops/plants?
2. Health: Condition
3. Issues: Diseases, pests
4. Recommendations: Actions (products, dosages)

Max {MAX_RESPONSE_LENGTH} words. No bold (**). Simple language."""
        
        content_parts = [prompt] + [resize_image(img) for img in images]
        
        response = model.generate_content(
            content_parts,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=IMAGE_ANALYSIS_MAX_TOKENS,
                temperature=TEMPERATURE_IMAGE_ANALYSIS,
            )
        )
        
        result = response.text if response and response.text else "Unable to analyze images."
        return remove_markdown_formatting(result)
    
    except Exception as e:
        return f"Error: {str(e)[:100]}"

def get_agriculture_response(user_message: str, weather_context: str = "", image_analysis: str = "") -> str:
    try:
        model = genai.GenerativeModel(GEMINI_MODEL)
        
        is_greeting = is_simple_greeting(user_message)
        current_season = get_indian_season()
        seasonal_crops = SEASONAL_CROPS.get(current_season, [])
        
        context = extract_context_from_history()
        has_enough_context = bool(context["location"] and context["soil_type"] and context["water_source"])
        
        conversation_history = ""
        if len(st.session_state.messages) > 1:
            recent = st.session_state.messages[-8:]
            history_parts = []
            for msg in recent:
                role = "Farmer" if msg["role"] == "user" else "Agent"
                content = msg['content'][:100]
                history_parts.append(f"{role}: {content}")
            conversation_history = "\n".join(history_parts)
        
        if is_greeting:
            system_prompt = """You are AgriAgent, AI agricultural assistant.

Simple greeting.

RULES:
- 30-50 words
- Warm and brief
- No bold (**)
- Just greet, ask how to help"""
        
        elif has_enough_context:
            system_prompt = f"""You are AgriAgent, expert consultant.

Farmer Context:
- Location: {context.get('location', 'Not specified')}
- Soil: {context.get('soil_type', 'Not specified')}
- Water: {context.get('water_source', 'Not specified')}
- Farm: {context.get('farm_size', 'Not specified')}
- Budget: {context.get('budget', 'Not specified')}
- Season: {current_season}
- Crops: {', '.join(seasonal_crops[:4])}

RULES:
1. Give RECOMMENDATIONS now
2. Max {MAX_RESPONSE_LENGTH} words
3. 2-3 crop suggestions with reasons
4. No bold (**)
5. Include costs, returns
6. One follow-up question

Previous:
{conversation_history}"""
        
        else:
            system_prompt = f"""You are AgriAgent, expert consultant.

Season: {current_season}
Need:
- Location: {context.get('location', 'NEEDED')}
- Soil: {context.get('soil_type', 'NEEDED')}
- Water: {context.get('water_source', 'NEEDED')}

RULES:
1. Ask MISSING info
2. 1-2 questions only
3. Max {MIN_RESPONSE_LENGTH} words
4. Conversational
5. No bold (**)

Previous:
{conversation_history}"""
        
        context_parts = [system_prompt]
        if weather_context and not is_greeting:
            context_parts.append(f"\nWeather: {weather_context}")
        if image_analysis:
            context_parts.append(f"\nImage: {image_analysis}")
        
        full_context = "\n\n".join(context_parts)
        
        response = model.generate_content(
            f"{full_context}\n\nQuery: {user_message}",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=200 if is_greeting else CHAT_MAX_TOKENS,
                temperature=0.9 if is_greeting else TEMPERATURE_CHAT,
            )
        )
        
        result = response.text if response and response.text else "I apologize, couldn't generate response."
        return remove_markdown_formatting(result)
    
    except Exception as e:
        return f"Error: {str(e)[:150]}"

def display_message(role: str, content: str, images: List[Image.Image] = None):
    import html
    safe_content = html.escape(content).replace('\n', '<br>')
    
    if role == "user":
        st.markdown(f"""
        <div class="message-container user-message">
            <div class="message-bubble user-bubble">
                {safe_content}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if images and len(images) > 0:
            if len(images) == 1:
                st.image(images[0], width=400)
            else:
                cols = st.columns(min(len(images), 3))
                for idx, img in enumerate(images):
                    with cols[idx % 3]:
                        st.image(img, use_container_width=True)
    else:
        st.markdown(f"""
        <div class="message-container">
            <div class="message-bubble assistant-bubble">
                {safe_content}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== HEADER ====================
st.markdown("""
<div style="position: fixed; top: 0; left: 0; right: 0; z-index: 999; 
            background: #0f1419; padding: 16px; text-align: center; 
            border-bottom: 1px solid #30363d;">
    <h1 style="font-size: 1.8em; font-weight: 700; color: #fff; margin: 0; letter-spacing: -0.5px;">
        🌾 AgriAgent
    </h1>
    <p style="color: #8b98a5; font-size: 0.9em; margin: 4px 0 0 0;">AI-Powered Agricultural Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ==================== CHAT DISPLAY ====================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-message">
        <h2>👋 Welcome to AgriAgent</h2>
        <p>Your AI-powered agricultural assistant. Ask me about crops, diseases, pests, or upload images for analysis. I can help with recommendations based on weather and season.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    display_messages = st.session_state.messages[-MAX_MESSAGES_DISPLAY:]
    for message in display_messages:
        display_message(
            message["role"], 
            message["content"], 
            message.get("images")
        )

st.markdown('</div>', unsafe_allow_html=True)

# ==================== INPUT AREA ====================
st.markdown('<div class="input-container"><div class="input-wrapper">', unsafe_allow_html=True)

# Paperclip icon
st.markdown('<div class="upload-btn">📎</div>', unsafe_allow_html=True)

col_input, col_clear = st.columns([10, 0.6])

with col_input:
    user_input = st.text_input(
        "Message",
        placeholder="Ask about crops, diseases, pests, or upload images...",
        key=f"user_input_{st.session_state.input_counter}",
        label_visibility="collapsed"
    )
    
    uploaded_files = st.file_uploader(
        "Upload",
        type=SUPPORTED_IMAGE_FORMATS,
        accept_multiple_files=True,
        key=f"file_upload_{st.session_state.input_counter}",
        label_visibility="collapsed"
    )

with col_clear:
    if st.button("🗑️", help="Clear"):
        st.session_state.messages = []
        st.session_state.weather_data = None
        st.session_state.processed_input = None
        st.session_state.context = {
            "location": None, "soil_type": None, "water_source": None,
            "budget": None, "experience": None, "farm_size": None
        }
        st.session_state.input_counter += 1
        st.rerun()

if uploaded_files:
    st.markdown(f'<span class="upload-badge">📷 {len(uploaded_files)} ready</span>', unsafe_allow_html=True)

st.markdown('</div></div>', unsafe_allow_html=True)

# ==================== PROCESS INPUT ====================
if user_input or uploaded_files:
    current_input_id = f"{user_input}_{len(uploaded_files) if uploaded_files else 0}_{st.session_state.input_counter}"
    
    if st.session_state.processed_input != current_input_id:
        st.session_state.processed_input = current_input_id
        
        weather_context = ""
        if user_input:
            location = extract_location_from_query(user_input)
            if location:
                with st.spinner("🌤️ Getting weather..."):
                    weather_data = get_weather_data(location)
                    if weather_data:
                        weather_context = format_weather_context(weather_data)
        
        image_analysis = ""
        image_objects = []
        
        if uploaded_files:
            try:
                for uploaded_file in uploaded_files:
                    file_size_mb = uploaded_file.size / (1024 * 1024)
                    if file_size_mb <= MAX_IMAGE_SIZE_MB:
                        image_objects.append(Image.open(uploaded_file))
                
                if image_objects:
                    st.session_state.messages.append({
                        "role": "user",
                        "content": user_input if user_input else f"📷 {len(image_objects)} image{'s' if len(image_objects) > 1 else ''}",
                        "images": image_objects.copy()
                    })
                    
                    with st.spinner("🔍 Analyzing..."):
                        query = user_input if user_input else "Analyze images"
                        image_analysis = analyze_images_with_gemini(image_objects, query)
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        elif user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
        
        query = user_input if user_input else "Analyze uploaded images."
        
        with st.spinner("🤖 Thinking..."):
            response = get_agriculture_response(query, weather_context, image_analysis)
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        st.session_state.input_counter += 1
        st.rerun()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="padding: 18px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 14px; color: white; margin-bottom: 20px;">
        <h2 style="margin: 0; font-size: 1.4em;">🌾 AgriAgent</h2>
        <p style="margin: 6px 0 0 0; opacity: 0.9; font-size: 0.85em;">AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Features")
    st.markdown("🌱 Crop recommendations")
    st.markdown("🐛 Disease diagnosis")
    st.markdown("📸 Image analysis")
    st.markdown("🌤️ Weather insights")
    st.markdown("💬 Natural chat")
    
    st.markdown("---")
    
    if st.session_state.weather_data:
        weather = st.session_state.weather_data
        st.markdown("### 🌍 Weather")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temp", f"{weather['main']['temp']}°C")
            st.metric("Humidity", f"{weather['main']['humidity']}%")
        with col2:
            st.metric("Wind", f"{weather['wind']['speed']} m/s")
            st.metric("Clouds", f"{weather['clouds']['all']}%")
        st.caption(f"📍 {weather['name']}")
        st.markdown("---")
    
    st.markdown("### 📊 Stats")
    st.metric("Messages", len(st.session_state.messages))
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("• Click 📎 to upload")
    st.markdown("• Mention location for weather")
    st.markdown("• Be specific about crops")
