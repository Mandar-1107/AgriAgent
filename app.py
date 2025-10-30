# app.py - AgriAgent (FINAL - All Issues Resolved)
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
    layout="wide",
    initial_sidebar_state="expanded"
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
    
    .main {
        background: #0f1419;
        min-height: 100vh;
        padding: 0 !important;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .chat-container {
        max-width: 850px;
        margin: 0 auto;
        padding: 100px 20px 160px 20px;
    }
    
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
        align-items: flex-end;
    }
    
    .stTextInput {
        flex: 1;
    }
    
    .stTextInput > div > div > input {
        border-radius: 24px !important;
        padding: 13px 20px !important;
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
    
    .stButton > button {
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        min-height: 46px !important;
        padding: 0 !important;
        font-size: 20px !important;
        border: 1px solid #30363d !important;
        background: #1c2128 !important;
        color: #8b98a5 !important;
        transition: all 0.2s !important;
        cursor: pointer !important;
    }
    
    .stButton > button:hover {
        background: #21262d !important;
        border-color: #484f58 !important;
        color: #e6edf3 !important;
        transform: scale(1.05);
    }
    
    /* Hide drag-drop area, show only Browse button */
    [data-testid="stFileUploadDropzone"] {
        display: none !important;
    }
    
    [data-testid="stFileUploaderDeleteBtn"] {
        display: none !important;
    }
    
    .stFileUploader {
        width: 46px !important;
        height: 46px !important;
    }
    
    .stFileUploader > div {
        width: 46px !important;
        height: 46px !important;
        padding: 0 !important;
    }
    
    .stFileUploader section {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
    
    .stFileUploader section button {
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        min-height: 46px !important;
        padding: 0 !important;
        border: 1px solid #30363d !important;
        background: #1c2128 !important;
        color: #8b98a5 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
        font-size: 0 !important;
    }
    
    .stFileUploader section button:hover {
        background: #21262d !important;
        border-color: #484f58 !important;
        color: #e6edf3 !important;
        transform: scale(1.05);
    }
    
    .stFileUploader section button::before {
        content: "📎";
        font-size: 20px;
        display: block;
    }
    
    .stFileUploader label {
        display: none !important;
    }
    
    .upload-badge {
        position: fixed;
        bottom: 80px;
        left: 50%;
        transform: translateX(-50%);
        padding: 8px 16px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        animation: slideUp 0.3s ease;
        z-index: 1001;
    }
    
    @keyframes slideUp {
        from { 
            opacity: 0; 
            transform: translateX(-50%) translateY(10px); 
        }
        to { 
            opacity: 1; 
            transform: translateX(-50%) translateY(0); 
        }
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    div[data-testid="stToolbar"] {display: none;}
    
    [data-testid="stSidebar"] {
        background: #0f1419 !important;
        border-right: 1px solid #30363d !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: #0f1419 !important;
        padding-top: 20px !important;
    }
    
    [data-testid="collapsedControl"] {
        background: #1c2128 !important;
        color: #e6edf3 !important;
        border: 1px solid #30363d !important;
        margin-top: 80px !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background: #667eea !important;
        color: #fff !important;
    }
    
    .app-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 998;
        background: #0f1419;
        padding: 16px 20px;
        border-bottom: 1px solid #30363d;
        text-align: center;
    }
    
    .app-header h1 {
        font-size: 1.8em;
        font-weight: 700;
        color: #fff;
        margin: 0;
    }
    
    .app-header p {
        color: #8b98a5;
        font-size: 0.9em;
        margin: 4px 0 0 0;
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
        "greeting_done": False,
        "location_asked": False,
        "user_declined_help": False,  # NEW: Track if user doesn't want help
        "context": {
            "location": None,
            "soil_type": None,
            "water_source": None,
            "budget": None,
            "experience": None,
            "farm_size": None,
            "active_farming": True
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
            
            # Check for explicit rejection
            if any(phrase in content_lower for phrase in ["no", "dont want", "don't want", "not interested", "stop asking"]):
                st.session_state.user_declined_help = True
            
            if any(phrase in content_lower for phrase in ["not growing", "giving time", "break", "replenish"]):
                context["active_farming"] = False
            
            location_keywords = ["maharashtra", "punjab", "karnataka", "gujarat", "rajasthan", 
                               "nagpur", "mumbai", "pune", "delhi", "bangalore"]
            
            if not context["location"]:
                for keyword in location_keywords:
                    if keyword in content_lower:
                        context["location"] = keyword
                        break
            
            if not context["soil_type"] and any(word in content_lower for word in ["clay", "sand", "loam", "soil"]):
                context["soil_type"] = content_lower
            
            if not context["water_source"] and any(word in content_lower for word in ["rain", "irrigation", "well"]):
                context["water_source"] = content_lower
            
            if not context["farm_size"] and any(word in content_lower for word in ["acre", "hectare"]):
                numbers = re.findall(r'\d+', content_lower)
                if numbers:
                    context["farm_size"] = f"{numbers[0]} acres"
    
    st.session_state.context = context
    return context

def is_simple_greeting(message: str) -> bool:
    greetings = ['hi', 'hello', 'hey', 'namaste']
    casual = ['how are you', 'what is your name']
    
    message_lower = message.lower().strip()
    
    if message_lower in greetings:
        return True
    
    for phrase in casual:
        if phrase in message_lower and len(message_lower) < 25:
            return True
    
    return False

def remove_markdown_formatting(text: str) -> str:
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    return text

def extract_location_from_query(query: str) -> Optional[str]:
    cities = ["mumbai", "delhi", "bangalore", "pune", "nagpur", "indore", "bhopal", "srinagar", "jammu"]
    states_to_cities = {
        "maharashtra": "mumbai", "punjab": "chandigarh", "karnataka": "bangalore",
        "gujarat": "ahmedabad", "rajasthan": "jaipur"
    }
    
    query_lower = query.lower()
    
    for city in cities:
        if city in query_lower:
            return city.title()
    
    for state, capital in states_to_cities.items():
        if state in query_lower:
            return capital.title()
    
    return None

def get_weather_data(location: str) -> Optional[Dict[str, Any]]:
    if not WEATHER_API_KEY:
        return None
    
    if (st.session_state.weather_data and 
        st.session_state.last_location and
        st.session_state.last_location.lower() == location.lower() and
        st.session_state.weather_cache_time and
        (datetime.now() - st.session_state.weather_cache_time).seconds < WEATHER_CACHE_DURATION):
        return st.session_state.weather_data
    
    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": f"{location},IN", "appid": WEATHER_API_KEY, "units": WEATHER_UNITS}
        response = requests.get(url, params=params, timeout=WEATHER_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.weather_data = data
            st.session_state.weather_cache_time = datetime.now()
            st.session_state.last_location = location
            return data
    except:
        pass
    
    return None

def format_weather_context(weather_data: Dict[str, Any]) -> str:
    if not weather_data:
        return ""
    
    try:
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        return f"Weather: {temp}°C, {humidity}% humidity."
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
        
        prompt = f"""Agricultural expert. Season: {season}. Query: "{query}"

Analyze and provide:
1. Crop/plant identification
2. Health condition
3. Diseases/pests
4. Recommendations of crops only once.
5. If user enters any irrelevant image content , politely decline the request
6. Don't recommend anything if user is already growing a crop 
Max {MAX_RESPONSE_LENGTH} words. Conversational."""
        
        content_parts = [prompt] + [resize_image(img) for img in images]
        
        response = model.generate_content(
            content_parts,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=IMAGE_ANALYSIS_MAX_TOKENS,
                temperature=0.7,
            )
        )
        
        result = response.text if response and response.text else "Unable to analyze."
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
        
        # If user has declined help multiple times, STOP asking
        if st.session_state.user_declined_help and len(st.session_state.messages) > 4:
            system_prompt = """You are AgriAgent, friendly consultant.

The user has declined further questions.

RULES:
- Give brief, helpful response (50-80 words)
- NO questions
- Just acknowledge and offer availability
- Be supportive and brief
- If user asks any other question than agriculture help , politely decline it"""
        
        elif not context["active_farming"]:
            system_prompt = f"""You are AgriAgent.

User wants to rest soil this season.

RULES:
- Support decision (it's smart!)
- Max {MAX_RESPONSE_LENGTH} words
- NO questions about farming details
- Brief and encouraging"""
        
        elif is_greeting and not st.session_state.greeting_done:
            st.session_state.greeting_done = True
            system_prompt = """You are AgriAgent.

First greeting.

RULES:
- 25-40 words
- Warm greeting
- Ask what they're growing
- Natural"""
        
        else:
            conversation_history = ""
            if len(st.session_state.messages) > 1:
                recent = st.session_state.messages[-4:]
                history_parts = []
                for msg in recent:
                    role = "F" if msg["role"] == "user" else "A"
                    content = msg['content'][:60]
                    history_parts.append(f"{role}: {content}")
                conversation_history = "\n".join(history_parts)
            
            known_count = sum([1 for v in [context["location"], context["water_source"]] if v])
            
            if known_count >= 1 and context["location"]:
                # Have location - give suggestions NOW
                system_prompt = f"""You are AgriAgent.

Farmer: {context.get('location', 'Unknown')} | Water: {context.get('water_source', 'Unknown')} | Season: {current_season}

RULES:
1. Give 2-3 crop recommendations (brief)
2. Max {MAX_RESPONSE_LENGTH} words
3. Mention costs/returns
4. ONE simple follow-up (not critical)
5. Natural tone

History:
{conversation_history}"""
            
            elif not st.session_state.location_asked:
                st.session_state.location_asked = True
                system_prompt = f"""You are AgriAgent.

Ask location naturally ONCE.

RULES:
- Ask where they're farming
- Max 50 words
- Conversational

History:
{conversation_history}"""
            
            else:
                # Already asked location - give general advice
                system_prompt = f"""You are AgriAgent.

Location already asked. Give general advice for {current_season}.

RULES:
- Suggest popular {current_season} crops
- Max {MAX_RESPONSE_LENGTH} words
- NO more questions
- Helpful and complete

History:
{conversation_history}"""
        
        context_parts = [system_prompt]
        if weather_context:
            context_parts.append(f"\n{weather_context}")
        if image_analysis:
            context_parts.append(f"\nImage: {image_analysis}")
        
        full_context = "\n\n".join(context_parts)
        
        response = model.generate_content(
            f"{full_context}\n\nUser: {user_message}",
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=180 if is_greeting else CHAT_MAX_TOKENS,
                temperature=0.8,
            )
        )
        
        result = response.text if response and response.text else "I'm here to help whenever you need advice!"
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
<div class="app-header">
    <h1>🌾 AgriAgent</h1>
    <p>AI Agricultural Assistant</p>
</div>
""", unsafe_allow_html=True)

# ==================== CHAT DISPLAY ====================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div class="welcome-message">
        <h2>👋 Welcome to AgriAgent</h2>
        <p>Your friendly AI agricultural assistant for crop advice, disease diagnosis, and farming guidance.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    display_messages = st.session_state.messages[-MAX_MESSAGES_DISPLAY:]
    for message in display_messages:
        display_message(message["role"], message["content"], message.get("images"))

st.markdown('</div>', unsafe_allow_html=True)

# ==================== INPUT AREA ====================
st.markdown('<div class="input-container"><div class="input-wrapper">', unsafe_allow_html=True)

col_input, col_upload, col_clear = st.columns([10, 0.7, 0.7])

with col_input:
    user_input = st.text_input(
        "Message",
        placeholder="Ask about crops, diseases, or farming advice...",
        key=f"user_input_{st.session_state.input_counter}",
        label_visibility="collapsed"
    )

with col_upload:
    uploaded_files = st.file_uploader(
        "Upload",
        type=SUPPORTED_IMAGE_FORMATS,
        accept_multiple_files=True,
        key=f"file_upload_{st.session_state.input_counter}",
        label_visibility="collapsed"
    )

with col_clear:
    if st.button("🗑️", help="Clear chat", key="clear_btn"):
        st.session_state.messages = []
        st.session_state.weather_data = None
        st.session_state.processed_input = None
        st.session_state.greeting_done = False
        st.session_state.location_asked = False
        st.session_state.user_declined_help = False
        st.session_state.context = {
            "location": None, "soil_type": None, "water_source": None,
            "budget": None, "experience": None, "farm_size": None, "active_farming": True
        }
        st.session_state.input_counter += 1
        st.rerun()

if uploaded_files and len(uploaded_files) > 0:
    st.markdown(f'<div class="upload-badge">📷 {len(uploaded_files)} ready</div>', unsafe_allow_html=True)

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
                    
                    with st.spinner("Analyzing..."):
                        query = user_input if user_input else "Analyze images"
                        image_analysis = analyze_images_with_gemini(image_objects, query)
            
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        elif user_input:
            st.session_state.messages.append({
                "role": "user",
                "content": user_input
            })
        
        if user_input or image_analysis:
            query = user_input if user_input else "Analyze images"
            
            with st.spinner("Thinking..."):
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
    <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 16px; color: white; margin-bottom: 24px; text-align: center;">
        <h2 style="margin: 0; font-size: 1.5em;">🌾 AgriAgent</h2>
        <p style="margin: 8px 0 0 0; opacity: 0.95; font-size: 0.9em;">AI Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ Features")
    st.markdown("""
    - 🌱 Crop recommendations
    - 🐛 Disease diagnosis  
    - 📸 Image analysis
    - 🌤️ Weather insights
    - 💬 Natural conversation
    """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Session")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Season", get_indian_season()[:8])
    
    if st.session_state.weather_data:
        st.markdown("---")
        weather = st.session_state.weather_data
        st.markdown("### 🌍 Weather")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Temp", f"{weather['main']['temp']}°C")
            st.metric("Humidity", f"{weather['main']['humidity']}%")
        with col2:
            st.metric("Wind", f"{weather['wind']['speed']} m/s")
            st.metric("Clouds", f"{weather['clouds']['all']}%")
        
        st.info(f"📍 {weather['name']}")
    
    st.markdown("---")
    st.caption("🌾 Made with ❤️ for farmers")
